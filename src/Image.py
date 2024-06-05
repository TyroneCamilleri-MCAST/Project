from ultralytics import YOLO

# model = YOLO(r"C:\Users\Abzsorb\Desktop\Mini-mapObjectDetection\src\CVModels\Ultralytics\Models\YOLO8N-COD6\weights\best.pt")
model = YOLO(r"C:\Users\Abzsorb\Desktop\Mini-mapObjectDetection\src\CVModels\Ultralytics\Models\Classification\Icon-Rotation-V16\weights\best.pt")

# source = r"C:\Users\Abzsorb\Desktop\Mini-mapObjectDetection\screenshots\20240526_205136\Image-5.png"
source = r"C:\Users\Abzsorb\Desktop\Mini-mapObjectDetection\screenshots\20240526_205136\Image-12.png"

results = model(source)  # list of Results objects

print(results)

