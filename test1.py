import qrcode
img = qrcode.make('https://nau3203-my.sharepoint.com/:b:/g/personal/umcr_na_edu/EdEHsxFVtm5HpjphrQnah9MBybazbwa1zCI6tUmENwqBEw?download=1')
type(img)  # qrcode.image.pil.PilImage
img.save("some_file.png")