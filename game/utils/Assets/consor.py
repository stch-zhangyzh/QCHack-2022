from PIL import Image

img = Image.open("consor.png")

out = img.resize((60,60))
out.save("new.png")