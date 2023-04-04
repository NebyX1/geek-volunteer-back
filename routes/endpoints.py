from flask import Blueprint, request, jsonify
from models.tables import Developer, Organization, UserInfo, Project, Review, Admin
from utils.db import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

api = Blueprint('api', __name__, url_prefix='/api')




#? Aquí se encuentran todos los endpoints relacionados con la tabla "Developer"

# Obtener todos los developers
@api.route('/developer', methods=['GET'])
def get_all_developers():
    all_developers = Developer.query.all()
    if all_developers:
        results = [developer.serialize() for developer in all_developers]
        return jsonify(results), 200
    else:
        return jsonify({"msg": "Aún no hay ningún developer creado"}), 404

# Crear un nuevo developer
@api.route('/developer', methods=['POST'])
def add_developer():
    user_name = request.json.get('user_name')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')
    password = request.json.get('password')
    avatar = request.json.get('avatar')

    existing_developer = Developer.query.filter_by(email=email).first()
    if existing_developer:
        return jsonify({"msg": "Ya existe un developer con ese email"}), 400

    new_developer = Developer(user_name=user_name, first_name=first_name,
                              last_name=last_name, email=email, password=password, avatar=avatar)

    try:
        db.session.add(new_developer)
        db.session.commit()
        return jsonify(new_developer.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return str(e), 500

# Eliminar un developer por su ID
@api.route('/developer/<int:developer_id>', methods=['DELETE'])
def delete_developer(developer_id):
    developer = Developer.query.get(developer_id)
    if not developer:
        return jsonify({"msg": "El developer seleccionado no existe"}), 404

    db.session.delete(developer)
    db.session.commit()
    return jsonify({"msg": "El developer ha sido eliminado con éxito"}), 200

# Modificar un developer por su ID
@api.route('/developer/<int:developer_id>', methods=['PUT'])
def update_developer(developer_id):
    developer = Developer.query.get(developer_id)
    if not developer:
        return jsonify({"msg": "El developer seleccionado no ha sido encontrado"}), 404

    data = request.get_json()
    developer.user_name = data.get('user_name', developer.user_name)
    developer.first_name = data.get('first_name', developer.first_name)
    developer.last_name = data.get('last_name', developer.last_name)
    developer.email = data.get('email', developer.email)
    developer.password = data.get('password', developer.password)
    developer.avatar = data.get('avatar', developer.avatar)

    db.session.commit()
    return jsonify(developer.serialize()), 200




#? Aquí se encuentran todos los endpoints relacionados con la tabla "Organization"

# Obtener todas las organizaciones
@api.route('/organization', methods=['GET'])
def get_all_organizations():
    all_organizations = Organization.query.all()
    if all_organizations:
        results = [organization.serialize() for organization in all_organizations]
        return jsonify(results), 200
    else:
        return jsonify({"msg": "Aún no hay ninguna organización creada"}), 404

# Crear una nueva organización
@api.route('/organization', methods=['POST'])
def add_organization():
    name = request.json.get('name')
    password = request.json.get('password')
    org_sector = request.json.get('org_sector')
    org_description = request.json.get('org_description')
    org_phone = request.json.get('org_phone')
    org_web = request.json.get('org_web')
    org_vision = request.json.get('org_vision')

    existing_organization = Organization.query.filter_by(name=name).first()
    if existing_organization:
        return jsonify({"msg": "Ya existe una organización con ese nombre"}), 400

    new_organization = Organization(name=name, password=password, org_sector=org_sector,
                                    org_description=org_description, org_phone=org_phone, org_web=org_web, org_vision=org_vision)

    try:
        db.session.add(new_organization)
        db.session.commit()
        return jsonify(new_organization.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return str(e), 500

# Eliminar una organización por su ID
@api.route('/organization/<int:organization_id>', methods=['DELETE'])
def delete_organization(organization_id):
    organization = Organization.query.get(organization_id)
    if not organization:
        return jsonify({"msg": "La organización seleccionada no existe"}), 404

    db.session.delete(organization)
    db.session.commit()
    return jsonify({"msg": "La organización ha sido eliminada con éxito"}), 200

# Modificar una organización por su ID
@api.route('/organization/<int:organization_id>', methods=['PUT'])
def update_organization(organization_id):
    organization = Organization.query.get(organization_id)
    if not organization:
        return jsonify({"msg": "La organización seleccionada no ha sido encontrada"}), 404

    data = request.get_json()
    organization.name = data.get('name', organization.name)
    organization.password = data.get('password', organization.password)
    organization.org_sector = data.get('org_sector', organization.org_sector)
    organization.org_description = data.get('org_description', organization.org_description)
    organization.org_phone = data.get('org_phone', organization.org_phone)
    organization.org_web = data.get('org_web', organization.org_web)
    organization.org_vision = data.get('org_vision', organization.org_vision)

    db.session.commit()
    return jsonify(organization.serialize()), 200




#? Aquí se encuentran todos los endpoints relacionados con la tabla "User_Info"

# Obtener todos los registros de información de usuario
@api.route('/user_info', methods=['GET'])
def get_all_user_info():
    all_user_info = UserInfo.query.all()
    if all_user_info:
        results = [user_info.serialize() for user_info in all_user_info]
        return jsonify(results), 200
    else:
        return jsonify({"msg": "Aún no hay ningún registro de información de usuario creado"}), 404

# Crear un nuevo registro de información de usuario
@api.route('/user_info', methods=['POST'])
def add_user_info():
    developer = request.json.get('developer')
    country = request.json.get('country')
    city = request.json.get('city')
    english_level = request.json.get('english_level')
    github_link = request.json.get('github_link')
    linkedin = request.json.get('linkedin')
    description = request.json.get('description')
    programing_languages = request.json.get('programing_languages')

    existing_user_info = UserInfo.query.filter_by(developer=developer).first()
    if existing_user_info:
        return jsonify({"msg": "Ya existe un registro de información para este usuario"}), 400

    new_user_info = UserInfo(developer=developer, country=country, city=city, english_level=english_level,
                             github_link=github_link, linkedin=linkedin, description=description, programing_languages=programing_languages)

    try:
        db.session.add(new_user_info)
        db.session.commit()
        return jsonify(new_user_info.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return str(e), 500

# Eliminar un registro de información de usuario por su ID
@api.route('/user_info/<int:user_info_id>', methods=['DELETE'])
def delete_user_info(user_info_id):
    user_info = UserInfo.query.get(user_info_id)
    if not user_info:
        return jsonify({"msg": "El registro de información de usuario seleccionado no existe"}), 404

    db.session.delete(user_info)
    db.session.commit()
    return jsonify({"msg": "El registro de información de usuario ha sido eliminado con éxito"}), 200

# Modificar un registro de información de usuario por su ID
@api.route('/user_info/<int:user_info_id>', methods=['PUT'])
def update_user_info(user_info_id):
    user_info = UserInfo.query.get(user_info_id)
    if not user_info:
        return jsonify({"msg": "El registro de información de usuario seleccionado no ha sido encontrado"}), 404

    data = request.get_json()
    user_info.developer = data.get('developer', user_info.developer)
    user_info.country = data.get('country', user_info.country)
    user_info.city = data.get('city', user_info.city)
    user_info.english_level = data.get('english_level', user_info.english_level)
    user_info.github_link = data.get('github_link', user_info.github_link)
    user_info.linkedin = data.get('linkedin', user_info.linkedin)
    user_info.description = data.get('description', user_info.description)
    user_info.programing_languages = data.get('programing_languages', user_info.programing_languages)

    db.session.commit()
    return jsonify(user_info.serialize()), 200




#? Aquí se encuentran todos los endpoints relacionados con la tabla "Project"

# Obtener todos los registros de proyectos
@api.route('/projects', methods=['GET'])
def get_all_projects():
    all_projects = Project.query.all()
    if all_projects:
        results = [project.serialize() for project in all_projects]
        return jsonify(results), 200
    else:
        return jsonify({"msg": "Aún no hay ningún proyecto creado"}), 404

# Crear un nuevo registro de proyecto
@api.route('/projects', methods=['POST'])
def add_project():
    organization = request.json.get('organization')
    project_name = request.json.get('project_name')
    project_description = request.json.get('project_description')
    latitude = request.json.get('latitude')
    longitude = request.json.get('longitude')
    done = request.json.get('done', False)
    developer_in_charge = request.json.get('developer_in_charge', None)

    new_project = Project(organization=organization, project_name=project_name, project_description=project_description,
                           latitude=latitude, longitude=longitude, done=done, developer_in_charge=developer_in_charge)

    try:
        db.session.add(new_project)
        db.session.commit()
        return jsonify(new_project.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return str(e), 500

# Eliminar un registro de proyecto por su ID
@api.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({"msg": "El proyecto seleccionado no existe"}), 404

    db.session.delete(project)
    db.session.commit()
    return jsonify({"msg": "El proyecto ha sido eliminado con éxito"}), 200

# Modificar un registro de proyecto por su ID
@api.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({"msg": "El proyecto seleccionado no ha sido encontrado"}), 404

    data = request.get_json()
    project.organization = data.get('organization', project.organization)
    project.project_name = data.get('project_name', project.project_name)
    project.project_description = data.get('project_description', project.project_description)
    project.latitude = data.get('latitude', project.latitude)
    project.longitude = data.get('longitude', project.longitude)
    project.done = data.get('done', project.done)
    project.developer_in_charge = data.get('developer_in_charge', project.developer_in_charge)

    db.session.commit()
    return jsonify(project.serialize()), 200




#? Aquí se encuentran todos los endpoints relacionados con la tabla "Review"

# Obtener todas las reviews
@api.route('/reviews', methods=['GET'])
def get_all_reviews():
    all_reviews = Review.query.all()
    if all_reviews:
        results = [review.serialize() for review in all_reviews]
        return jsonify(results), 200
    else:
        return jsonify({"msg": "Aún no hay ninguna review creada"}), 404

# Crear una nueva review
@api.route('/reviews', methods=['POST'])
def add_review():
    organization = request.json.get('organization')
    developer = request.json.get('developer')
    project = request.json.get('project')
    stars = request.json.get('stars')
    comment = request.json.get('comment')

    new_review = Review(organization=organization, developer=developer, project=project,
                         stars=stars, comment=comment)

    try:
        db.session.add(new_review)
        db.session.commit()
        return jsonify(new_review.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return str(e), 500




#? Aquí se encuentran todos los endpoints relacionados con la tabla "Admin"

# Obtener información de un admin por su ID
@api.route('/admins/<int:admin_id>', methods=['GET'])
def get_admin(admin_id):
    admin = Admin.query.get(admin_id)
    if not admin:
        return jsonify({"msg": "El administrador seleccionado no existe"}), 404
    else:
        return jsonify(admin.serialize()), 200