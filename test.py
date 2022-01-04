from pathlib import Path
from shutil import copy

i = 0

for path in Path('images/pm_apk').rglob('**/*.xml'):
    print(path)
    # copy(path, f"images/apk_ui/{path.name}")
    i+=1
    print(i)

    import cv2

# image = cv2.imread('1.jpg')
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur(gray, (5,5), 0)
# thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if len(cnts) == 2 else cnts[1]
# for c in cnts:
#     area = cv2.contourArea(c)
#     if area > 10000:
#         cv2.drawContours(image, [c], -1, (36,255,12), 3)

# cv2.imwrite('thresh.png', thresh)
# cv2.imwrite('image.png', image)
# cv2.waitKey()