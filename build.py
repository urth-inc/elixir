#!/usr/bin/env python3

import argparse
import tomllib
import subprocess
from typing import Dict, Any


def load_versions(toml_file: str) -> Dict[str, Any]:
    """バージョン情報をTOMLファイルから読み込む"""
    with open(toml_file, "rb") as f:
        return tomllib.load(f)


def build_docker_image(versions: Dict[str, Any], args: argparse.Namespace) -> None:
    """Dockerイメージをビルドする"""
    # バージョン情報の取得
    elixir_info = versions["versions"]["elixir"][args.elixir]
    erlang_info = versions["versions"]["erlang"][args.erlang]

    # タグの生成
    tag = (
        f"{args.repository}/elixir:{args.elixir}-otp-{args.erlang}-ubuntu-{args.ubuntu}"
    )

    # Dockerビルドコマンドの構築
    cmd = [
        "docker",
        "build",
        "--build-arg",
        f"UBUNTU_VERSION={args.ubuntu}",
        "--build-arg",
        f"ELIXIR_VERSION=v{args.elixir}",
        "--build-arg",
        f"ERLANG_VERSION={args.erlang}",
        "--build-arg",
        f"ELIXIR_DOWNLOAD_URL={elixir_info['url']}",
        "--build-arg",
        f"ELIXIR_DOWNLOAD_SHA256={elixir_info['sha256']}",
        "--build-arg",
        f"ERLANG_DOWNLOAD_URL={erlang_info['url']}",
        "--build-arg",
        f"ERLANG_DOWNLOAD_SHA256={erlang_info['sha256']}",
        "-t",
        tag,
        ".",
    ]

    # ビルドの実行
    print(f"Building Docker image: {tag}")
    subprocess.run(cmd, check=True)

    # プッシュが指定されている場合
    if args.push:
        print(f"Pushing Docker image: {tag}")
        subprocess.run(["docker", "push", tag], check=True)


def main():
    parser = argparse.ArgumentParser(description="Build Elixir Docker image")
    parser.add_argument("--elixir", default="1.12.3", help="Elixir version")
    parser.add_argument("--erlang", default="23.3", help="Erlang version")
    parser.add_argument("--ubuntu", default="20.04", help="Ubuntu version")
    parser.add_argument(
        "--repository", default="ghcr.io/urth-inc", help="Docker repository"
    )
    parser.add_argument(
        "--versions-file", default="versions.toml", help="Path to versions.toml"
    )
    parser.add_argument("--push", action="store_true", help="Push image after building")
    args = parser.parse_args()

    try:
        versions = load_versions(args.versions_file)
        build_docker_image(versions, args)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
