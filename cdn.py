from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from imagekitio import ImageKit
import base64


imagekit = ImageKit(
    private_key='private_Unb8Yg+MvyUKRGLbP7pmYHUjXcE=',
    public_key='public_CTihP5oL+OaJ2BcDEwijHVEHZwU=',
    url_endpoint='https://ik.imagekit.io/njtsu3vzq'
)



def upload_file(file):
    with open(file,"rb")as f:
        a = base64.b64encode(f.read())
        result = imagekit.upload_file(file=a, # required
                                file_name='image.jpg', # required
                                )
    return result.url

if __name__ == "__main__":
    print(upload_file("test_render68.jpg"))