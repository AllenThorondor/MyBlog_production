from flask import render_template, request, redirect, url_for, Blueprint
from flaskblog import db
from flaskblog.models import Friend
from flaskblog.face.forms import FaceForm
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from PIL import Image, ImageDraw
import numpy as np

face = Blueprint('face', __name__)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + str(f_ext)
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    picture_path_short = os.path.join('../static/profile_pics', picture_fn)

    output_size = (1200, 1200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_path_short, picture_path


@face.route('/face_recognition', methods=["GET", "POST"])
def face_recognition():
    form = FaceForm()
    if form.validate_on_submit():
        _, picture_path1 = save_picture(form.picture1.data)
        path2_short, picture_path2 = save_picture(form.picture2.data)
        print(picture_path1)
        print(picture_path2)
        import face_recognition
        test1 = face_recognition.load_image_file(picture_path1)
        test1_face_encoding = face_recognition.face_encodings(test1)[0]
        known_face_encodings = [test1_face_encoding]
        known_face_names = ["target"]
        print("ok, the known_face_encodings is done")
        unknown_image = face_recognition.load_image_file(picture_path2)
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
        pil_image = Image.fromarray(unknown_image)
        draw = ImageDraw.Draw(pil_image)
        print("ok, the unknown_face_encodings is done")
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            # Draw a box around the face using the Pillow module
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

            # Draw a label with a name below the face
            text_width, text_height = draw.textsize(name)
            draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
            draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
        del draw
        form.path = path2_short
        pil_image.save(picture_path2)
        # pil_image.show()
    return render_template('face.html', title='face_recognition', form=form)
