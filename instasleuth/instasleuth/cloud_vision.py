def cloud_api(file_name):
    import io
    import json
    from google.cloud import vision
    from google.cloud.vision import types

    vision_client = vision.Client.from_service_account_json('/var/www/apikey.json')

    with io.open(file_name,'rb') as image_file:
           content = image_file.read();
           image= vision_client.image(content=content)

    # labels 
    labels = image.detect_labels()
    datalabels ={}
    for label in labels:
           datalabels[label.description]=label.score
    json_label = json.dumps(datalabels)
    print (json_label)


    # textdetection 
    def detect_text(path):
        """Detects text in the file."""
        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations
        print('Texts:')

        list_of_texts = []
        for text in texts:
            print('\n"{}"'.format(text.description))
            list_of_texts.append(text.description)
            vertices = (['({},{})'.format(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices])

            print('bounds: {}'.format(','.join(vertices)))
        print list_of_texts, "list_of_texts"
        return list_of_texts
    return detect_text(file_name)
