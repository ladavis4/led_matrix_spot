from PIL import Image
import requests
from io import BytesIO


class spotifyCaller():
    def __init__(self):
        pass

    def get_current_img(self):  # Function pulls tract number from census website given lat/lon.
        # Create the custom url
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer BQDspLVRsNxnyC4FdgGvulrz7rVYKCfaJwHj5IqZWrH8wzfdj1YdKZQlf39E_7k9PJErsRCJZQFjDEwtY3kfR1hGuL-U_mv8QS3RXXXHAY_un0dOqkws7oBuBr-FqOu2HouMumuVTQEYnUH4CdVv9XSMYd4PyXQtvA6RK7D4yqnFEw',
        }
        params = (('market', 'ES'),)
        response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers,
                                params=params)
        data = response.json()
        url = data['item']['album']['images'][2]['url']
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        return img


if __name__ == "__main__":
    caller = spotifyCaller()
    img = caller.get_current_img()
    img.show()

