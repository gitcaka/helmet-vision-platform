import argparse
import getpass
import os
import sys

from app import app
from models import User, db


def parse_args():
    parser = argparse.ArgumentParser(description="初始化 helmet-flask SQLite 数据库")
    parser.add_argument(
        "--username",
        default=os.getenv("HELMET_ADMIN_USERNAME", "admin"),
        help="管理员用户名，默认 admin",
    )
    parser.add_argument(
        "--password",
        default=os.getenv("HELMET_ADMIN_PASSWORD"),
        help="管理员密码；省略时在终端安全输入",
    )
    parser.add_argument(
        "--reset-password",
        action="store_true",
        help="用户已存在时更新密码",
    )
    return parser.parse_args()


def read_password(provided_password):
    if provided_password:
        return provided_password

    password = getpass.getpass("管理员密码：")
    confirmation = getpass.getpass("再次输入密码：")
    if password != confirmation:
        raise ValueError("两次输入的密码不一致")
    return password


def main():
    args = parse_args()
    username = args.username.strip()
    password = read_password(args.password)

    if not username:
        raise ValueError("用户名不能为空")
    if len(password) < 8:
        raise ValueError("密码至少需要 8 个字符")

    with app.app_context():
        db.create_all()
        user = User.query.filter_by(username=username).first()
        if user and not args.reset_password:
            print(f"数据库已存在用户 {username}，未修改密码。")
        else:
            created = user is None
            if user is None:
                user = User(username=username)
                db.session.add(user)
            user.set_password(password)
            db.session.commit()
            action = "创建" if created else "更新"
            print(f"已{action}管理员用户：{username}")

        print(f"SQLite 数据库：{app.config['DATABASE_PATH']}")


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"初始化失败：{exc}", file=sys.stderr)
        raise SystemExit(2) from exc
