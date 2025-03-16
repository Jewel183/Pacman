from PIL import Image, ImageDraw, ImageFont

FONT = r"E:\\2024-2025\\HK2_2024-2025\\AI\\Project01\\Project-Search-Pacman\\Font\\Pixelfy.ttf"

# Tạo ảnh mới
image = Image.new('RGB', (800, 600), (0, 0, 0))  # Màu nền đen
draw = ImageDraw.Draw(image)

# Sử dụng phông chữ pixel (PressStart2P.ttf)
font = ImageFont.truetype(FONT, 50)

# Vẽ tiêu đề
draw.text((100, 100), "Pixel Game", font=font, fill=(255, 255, 255))  # Màu trắng

# Hiển thị ảnh
image.show()
