import os
import secrets

from fastapi import HTTPException
from sqlalchemy import select

from auth.requests import PackageRequest
from core.dafunk import Protocol, Request
from models import User, Packages, PackagesPermissions
from auth.service import service
service_path = os.path.dirname(os.path.abspath(__file__))

def main():
    @service.route("/auth/key",
                   request=Request.POST,
                   protocol=Protocol.WEB
                   )
    async def key_generate(package: PackageRequest):
        session = service.db.get_session()
        stmt = select(Packages).where(Packages.name == package.name)
        package_obj = session.scalars(stmt).one_or_none()
        if package_obj is None:
            return HTTPException(status_code=404, detail="Package not found")
        else:
            key = secrets.token_urlsafe(16)
            key_obj = User(key=key, package=package_obj)
            session.add(key_obj)
        session.commit()
        session.close()
        return {"key": key}

    @service.route("/auth/package",
                   request=Request.POST,
                   protocol=Protocol.WEB
                   )
    async def package_generate(package: PackageRequest):
        session = service.db.get_session()
        stmt = select(Packages).where(Packages.name == package.name)
        package_obj = session.scalars(stmt).one_or_none()
        if package_obj is not None:
            return HTTPException(status_code=400, detail="Package name already exist")
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
        return {"id": pkg_obj.id, "name": pkg_obj.name}

    service.start(
        events_processes=False, web_processes=True
    )

if __name__ == '__main__':
    main()