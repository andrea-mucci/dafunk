import os
import secrets
from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from starlette.authentication import requires


from auth.requests import PackageRequest, KeyRequest, PermissionsRequest
from core.dafunk import Protocol, HttpRequest, Request
from core.dafunk.models import Packages, User, PackagesPermissions
from auth.service import service


service_path = os.path.dirname(os.path.abspath(__file__))

def main():
    @service.route("/auth/key",
                   request=HttpRequest.POST,
                   protocol=Protocol.WEB
                   )
    @requires(['admin'])
    async def key_generate(package: KeyRequest, request: Request):
        session = service.db.get_session()
        stmt = select(Packages).where(Packages.name == package.package)
        package_obj = session.scalars(stmt).one_or_none()
        if package_obj is None:
            return HTTPException(status_code=404, detail="Package not found")
        else:
            key = secrets.token_urlsafe(125)
            key_obj = User(key=key, package=package_obj)
            session.add(key_obj)

        # send message to the broker
        service.send_event("user.added", {
            "key": key,
            "package": package_obj.name,
        })
        session.commit()
        session.close()
        return {"key": key}

    @service.route("/auth/package",
                   request=HttpRequest.POST,
                   protocol=Protocol.WEB
                   )
    async def package_generate(package: PackageRequest):
        session = service.db.get_session()
        stmt = select(Packages).where(Packages.name == package.name)
        package_obj = session.scalars(stmt).one_or_none()
        if package_obj is not None:
            return HTTPException(status_code=404, detail="Package name already exist")
        else:
            pkg_obj = Packages(name=package.name)
            session.add(pkg_obj)
            for permission in package.permissions:
                session.add(PackagesPermissions(
                    package=pkg_obj,
                    scope=permission.scope,
                    value=permission.value
                ))
        session.commit()
        session.close()
        dict_package = package.model_dump()
        return_object = {
            "name": dict_package["name"],
            "permissions": dict_package['permissions'],
        }
        service.send_event("package.added", return_object)
        return return_object

    @service.route("/auth/package/{package_name}",
                   request=HttpRequest.PUT,
                   protocol=Protocol.WEB
                   )
    async def package_update(package_name: str, permissions: List[PermissionsRequest]):
        session = service.db.get_session()
        stmt = select(Packages).where(Packages.name == package_name)
        package_obj = session.scalars(stmt).one_or_none()
        if package_obj is None:
            return HTTPException(status_code=404, detail="Package does not exist")
        else:
            for permission in permissions:
                pkg_stmt = select(PackagesPermissions).where(PackagesPermissions.scope == permission.scope).where(
                    PackagesPermissions.package == package_obj
                )
                perm = session.scalars(pkg_stmt).one_or_none()
                if perm is None:
                    # add new permission
                    perm_pkg = PackagesPermissions(package=package_obj, scope=permission.scope, value=permission.value)
                    session.add(perm_pkg)
                else:
                    # update the permission
                    perm.value = permission.value
                    perm.scope = permission.scope

        session.commit()
        session.close()
        return {}

    @service.route("/auth/package/{package_name}",
                   request=HttpRequest.GET,
                   protocol=Protocol.WEB
                   )
    async def package_get(package_name: str):
        session = service.db.get_session()
        stmt = select(Packages).where(Packages.name == package_name)
        package_obj = session.scalars(stmt).one_or_none()
        if package_obj is None:
            return HTTPException(status_code=404, detail="Package does not exist")

        data = {
            "id": package_obj.id,
            "name": package_obj.name,
            "permissions": []
        }
        for permission in package_obj.permissions:
            data["permissions"].append({
                "scope": permission.scope,
                "value": permission.value
            })
        session.close()
        return data

    @service.route("/auth/package/{package_name}",
                   request=HttpRequest.DELETE,
                   protocol=Protocol.WEB
                   )
    async def package_delete(package_name: str):
        session = service.db.get_session()
        stmt = select(Packages).where(Packages.name == package_name)
        package_obj = session.scalars(stmt).one_or_none()
        if package_obj is None:
            return HTTPException(status_code=404, detail="Package does not exist")
        session.delete(package_obj)
        session.commit()
        session.close()
        return {}

    service.start(
        events_processes=False, web_processes=True
    )

if __name__ == '__main__':
    main()