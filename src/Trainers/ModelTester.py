import os
import time
from PIL import Image
import gradio as gr
from ultralytics import YOLO
import cv2

# Define the base directories for models
base_dir = r"./Models"
object_detection_dir = os.path.join(base_dir, "object_detection")
classification_dir = os.path.join(base_dir, "classification")

classes = ['top', 'top_rights', 'top_right', 'left', 'right', 'bottom', 'bottom_left', 'bottom_right']

def generate_model_paths(base_dir):
    model_paths = {}
    for subfolder in os.listdir(base_dir):
        subfolder_path = os.path.join(base_dir, subfolder)
        weight_path = os.path.join(subfolder_path, "weights", "best.pt")
        if os.path.isdir(subfolder_path) and os.path.exists(weight_path):
            model_paths[subfolder] = weight_path
    return model_paths

model_paths = generate_model_paths(object_detection_dir)
classification_model_paths = generate_model_paths(classification_dir)

def predict_image(model_name, classification_model_name, task, image):
    try:
        timestamp = int(time.time())
        output_image_path = f"output_image_{timestamp}.jpg"
        top1 = -1

        if task in ["Object Detection", "Both"]:
            model = YOLO(model_paths[model_name])
            results = model(image)
            for r in results:
                im_array = r.plot()  # plot a BGR numpy array of predictions
                im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
                im.save(output_image_path)  # save image

        if task in ["Classification", "Both"]:
            class_model = YOLO(classification_model_paths[classification_model_name])
            class_results = class_model(image)
            for r in class_results:
                top1 = r.probs.top1
                im_array = r.plot()  # plot a BGR numpy array of predictions
                im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
                im.save(output_image_path)  # save image

        result = (output_image_path, "No Classification Was Found" if top1 == -1 else classes[top1])
        return result
    except Exception as e:
        print(f"Error in predict_image: {e}")
        return None, None

def process_video(model_name, classification_model_name, task, video_path):
    try:
        # Load object detection model
        object_detection_model = YOLO(model_paths[model_name]) if task in ["Object Detection", "Both"] else None
        # Load classification model
        classification_model = YOLO(classification_model_paths[classification_model_name]) if task in ["Classification", "Both"] else None

        # Open the video file
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("Error: Could not open video.")
            return None

        frame_count = 0
        total_detection_time = 0
        total_classification_time = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            start_time = time.time()

            # Perform object detection
            if object_detection_model:
                detection_start = time.time()
                results = object_detection_model(frame)
                detection_end = time.time()
                total_detection_time += (detection_end - detection_start)

                for r in results:
                    frame = r.plot()  # plot results on frame

            # Perform classification
            if classification_model:
                classification_start = time.time()
                class_results = classification_model(frame)
                classification_end = time.time()
                total_classification_time += (classification_end - classification_start)

                for r in class_results:
                    top1 = r.probs.top1
                    label = classes[top1] if top1 != -1 else "No Classification Found"
                    # Draw the classification label on the frame
                    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            end_time = time.time()

            # Calculate FPS
            frame_processing_time = end_time - start_time
            fps = 1 / frame_processing_time if frame_processing_time > 0 else 0

            # Display the frame
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow('Video', frame)

            frame_count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return f"Video Finished."
    except Exception as e:
        print(f"Error in process_video: {e}")
        return None

image_interface = gr.Interface(
    fn=predict_image,
    inputs=[
        gr.Dropdown(choices=list(model_paths.keys()), label="Model"),
        gr.Dropdown(choices=list(classification_model_paths.keys()), label="Classification Model"),
        gr.Radio(choices=["Object Detection", "Classification", "Both"], label="Task"),
        gr.Image(type="pil", label="Input Image"),
    ],
    outputs=[gr.Image(type="filepath", label="Output Image"), gr.Text(label="Classification")]
)

video_interface = gr.Interface(
    fn=process_video,
    inputs=[
        gr.Dropdown(choices=list(model_paths.keys()), label="Model"),
        gr.Dropdown(choices=list(classification_model_paths.keys()), label="Classification Model"),
        gr.Radio(choices=["Object Detection", "Classification", "Both"], label="Task"),
        gr.Video(label="Input Video"),
    ],
    outputs="text"
)

# tabbed = gr.TabbedInterface([image_interface, video_interface], ["Image", "Video"])

if __name__ == "__main__":
    # tabbed.launch(debug=True, show_error=True)
    video_interface.launch()
