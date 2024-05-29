from auth_middleware import token_required
import jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource
from model.users import User
from __init__ import db

user_api = Blueprint('user_api', __name__, url_prefix='/api/users')
api = Api(user_api)

class UserAPI:
    class _Image(Resource):
        def get(self):
            image_data = User.query.with_entities(User._image).all()
            json_ready = [row[0] for row in image_data]
            print(json_ready)
            return jsonify(json_ready)

        def post(self):
            token = request.cookies.get('jwt')
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"]) 
            useruid = data["_uid"]
            users = User.query.all()
            for user in users:
                if user.uid == useruid:
                    print(user.text)

        def put(self):
            body = request.get_json()
            token = request.cookies.get("jwt")
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            image = body.get('image')
            users = User.query.all()
            print(data)
            for user in users:
                if user.uid == data["_uid"]:
                    print(data["_uid"])
                    user.update("", "", "", user._image + "///" + image, user._role)
                    print(image)
                    print(user._image)
                    
        def delete(self):
            try:
                token = request.cookies.get('jwt')
                data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"]) 
                useruid = data["_uid"]

                # Assuming you have a method to get the current user based on uid
                user = User.query.filter_by(_uid=useruid).first()

                if user:
                    # Your image deletion logic here
                    # For example, assuming you store images in the database, you can remove the image attribute
                    user.image = ''
                    db.session.commit()

                    return {'message': 'Image deleted successfully'}, 200
                else:
                    return {'error': 'User not found'}, 404
            except Exception as e:
                return {'error': str(e)}, 500


    class _Name(Resource):
        def get(self):
            name_data = User.query.with_entities(User._name).all()
            json_ready = [row[0] for row in name_data]
            print(json_ready)
            return jsonify(json_ready)
        def put(self):
            body = request.get_json()
            uid = body.get('uid')
            new_name = body.get('new_name')

            # Check if the user exists
            user = User.query.filter_by(_uid=uid).first()
            if not user:
                return {'error': 'User not found'}, 404

            # Update the user's name
            user._name = new_name
            db.session.commit()

            return {'message': 'Username updated successfully'}, 200

    class _CRUD(Resource):
        def post(self):
            body = request.get_json()
            print(body)
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            password = body.get('password')
            uo = User(name=name, uid=uid)
            if password is not None:
                uo.set_password(password)
            user = uo.create()
            if user:
                print(user.read())
                return ((user.read()), 200)
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

        @token_required
        def get(self, current_user):
            users = User.query.all()
            json_ready = [user.read() for user in users]
            return jsonify(json_ready)

        @token_required
        def delete(self, current_user):
            body = request.get_json()
            uid = body.get('uid')
            users = User.query.all()
            for user in users:
                if user.uid == uid:
                    user.delete()
            return jsonify(user.read())

        @token_required
        def put(self, current_user):
            body = request.get_json()
            uid = body.get('uid')
            name = body.get('name')
            image = body.get('image')
            theme = body.get('theme')  # Added theme update
            users = User.query.all()
            for user in users:
                if user.uid == uid:
                    user.update(name, '', '', image, user.role)
                    user.theme = theme  # Set the theme
                    db.session.commit()  # Commit the changes to the database
            return f"{user.read()} Updated"

    class _Security(Resource):
        def post(self):
            try:
                body = request.get_json()
                print(body)
                if not body:
                    return {
                        "message": "Please provide user details",
                        "data": None,
                        "error": "Bad request"
                    }, 400
                uid = body.get('uid')
                if uid is None:
                    print("error at uid")
                    return {'message': f'User ID is missing'}, 400
                password = body.get('password')
                user = User.query.filter_by(_uid=uid).first()
                if user is None or not user.is_password(password):
                    print("error at password")
                    return {'message': f"Invalid user id or password"}, 401
                if user:
                    try:
                        token = jwt.encode(
                            {"_uid": user._uid},
                            current_app.config["SECRET_KEY"],
                            algorithm="HS256"
                        )
                        resp = Response("Authentication for %s successful" % (user._uid))
                        resp.set_cookie(key="jwt", value=token, max_age=3600, secure=True, samesite="None", path='/', httponly=False)
                        print(resp.headers) 
                        return resp
                    except Exception as e:
                        return {
                            "error": "Something went wrong",
                            "message": str(e)
                        }, 500
                return {
                    "message": "Error fetching auth token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 404

            except Exception as e:
                return {
                        "message": "Something went wrong!",
                        "error": str(e),
                        "data": None
                }, 500

    class _TextUpload(Resource):
        def post(self):
            data = request.get_json()
            text_content = data.get('text_content')

            if not text_content:
                return {'message': 'Text content is missing'}, 400

            text_upload = TextUpload.create(text_content)

            if text_upload:
                return jsonify({'message': 'Text uploaded successfully'}), 200
            else:
                return {'message': 'Error uploading text'}, 500
    class _AllRatings(Resource):
        def get(self):
            Users = User.query.all()
            ratings = {}
            for user in Users:
                if user._ratings:
                    for rating in user._ratings.split():
                        recipe_id, star_count = rating.split(":")
                        star_count = int(star_count)
                        if recipe_id not in ratings or ratings[recipe_id]['starCount'] < star_count:
                            ratings[recipe_id] = {
                                "uid": user._name,
                                "starCount": star_count
                            }
            return jsonify(ratings)

    class _Recipe(Resource):
        def get(self):
            Users = User.query.all()
            resp = []
            for user in Users:
                if user.ratings:
                    resp.append((user.ratings, user._uid))
            print(resp)
            return jsonify(resp)

        def post(self):
            data = request.get_json()
            print(data)
            user = User.query.filter_by(_uid=data.get("uid")).first()
            if not user:
                return {"message": "User not found!"}, 404

            id_to_update = data.get("id")
            star_count = data.get("starCount")

            if not id_to_update or star_count is None:
                return {"message": "Invalid data!"}, 400

            updated_ratings = f"{id_to_update}:{star_count}"
            if user._ratings:
                user._ratings += f" {updated_ratings}"
            else:
                user._ratings = updated_ratings

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {"message": "An error occurred while updating ratings!"}, 500

            return {"message": "Ratings updated successfully!"}, 200

    class _Settings(Resource):
        def post(self):
            data = request.json.get('settings')
            uid = data.get('uid')
            username = data.get('name')
            password = data.get('password')
            theme = data.get('theme')

            # Check if the provided user credentials match an existing user in the database
            user = User.query.filter_by(_uid=uid).first()
            print(user) 
            if user is None or not user.is_password(password) or user.name != username:
                return {'error': 'Invalid user credentials or theme'}, 400
            
            # Check if the theme is 'light' or 'dark'
            if theme not in ['light', 'dark']:
                return {'error': 'Invalid theme specified'}, 400
            
            # Update the user's theme setting
            user.theme = theme
            db.session.commit()

            return {'message': 'Settings saved successfully'}, 200
    api.add_resource(_AllRatings, '/ratings')
    api.add_resource(_Image, '/image')
    api.add_resource(_Name, '/name')
    api.add_resource(_CRUD, '/')
    api.add_resource(_Security, '/authenticate')
    api.add_resource(_TextUpload, '/upload/text')
    api.add_resource(_Settings, '/save_settings')
    api.add_resource(_Recipe, '/recipe')
