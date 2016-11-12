# URL Uploader

This example script shows how the Gfycat API can be used to fetch videos or gifs from a list of URLs and convert them to gfycats.

## Usage

The script takes 3 parameters:
 - **client_id** - The id of the oauth2 client assigned when the client was registered.
 - **client_secret** - The secret of the oauth2 client assigned when the client was registered.
 - **input** - The path of a JSON file that describes which urls to fetch from and what parameters to use.

## Example
```bash
./url_uploader.py --client_id 2_eybdM- --client_secret O0hsP5V6UgV-JmZIBox9uR6q3xBwO3OBH8TQ0eCqon4sbjFfB4l8PVuC3-AlR4wp --input input.json
```

## JSON format
The input JSON file schema can be found on the Gfycat API reference page under the section [Gfycat creation parameters and options](http://developers.gfycat.com/api/#gfycat-creation-parameters-and-options).
An example of the input array is in sample_urls.json.  Further details, such as title, tags, captions, etc can be added according to the api docs.
