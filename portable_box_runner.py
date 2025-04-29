import os
import sys
import yaml
import time
import logging
from pathlib import Path
# from boxsdk import Client, OAuth2  # 実装時に有効化

def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def box_authenticate(client_id, client_secret):
    # Box認証のダミー実装
    print("Box認証（ダミー）: client_id={}, client_secret={}".format(client_id, client_secret))
    # return Client(OAuth2(...))
    return None

def get_box_file_list(folder_id):
    # Boxフォルダ内ファイル一覧取得（ダミー）
    print(f"Boxフォルダ({folder_id})のファイル一覧取得（ダミー）")
    # 実際はAPIで取得
    return [
        {"name": "MyApp.exe", "id": "111", "size": 123456, "sha1": "dummysha1"},
        {"name": "readme.txt", "id": "112", "size": 100, "sha1": "dummysha2"},
    ]

def compare_and_get_diff(box_files, local_dir):
    # 差分比較（ダミー）
    print(f"ローカル({local_dir})とBoxの差分比較（ダミー）")
    # 実際はファイル存在・サイズ・ハッシュ比較
    return box_files  # すべてダウンロード対象とする

def download_files(diff_files, local_dir):
    # 差分ファイルのみダウンロード（ダミー）
    for f in diff_files:
        print(f"ダウンロード: {f['name']} -> {local_dir}")
        # 実際はAPIでダウンロード
        Path(local_dir).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(local_dir, f["name"]), "w") as fp:
            fp.write("dummy content")

def launch_app(exe_path):
    print(f"アプリ起動: {exe_path}")
    # 実際はsubprocessで起動、多重起動防止等
    # subprocess.Popen([exe_path])

def setup_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )

def main():
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"
    if not os.path.exists(config_path):
        print(f"設定ファイルが見つかりません: {config_path}")
        print("カレントディレクトリまたは引数で設定ファイルパスを指定してください。")
        print("サンプル設定ファイル例:")
        print("""
box:
  client_id: "xxxxxxxx"
  client_secret: "xxxxxxxx"
  folder_id: "1234567890"
local:
  sync_dir: "C:/PortableApps/MyApp"
  exe_name: "MyApp.exe"
sync:
  interval_min: 60
  delete_orphan: false
log:
  file: "runner.log"
""")
        sys.exit(1)
    config = load_config(config_path)
    setup_logger(config["log"]["file"])
    logging.info("PortableBoxRunner 起動")

    box_cfg = config["box"]
    local_cfg = config["local"]
    sync_cfg = config["sync"]

    # Box認証
    client = box_authenticate(box_cfg["client_id"], box_cfg["client_secret"])

    # Boxフォルダ内ファイル一覧取得
    box_files = get_box_file_list(box_cfg["folder_id"])

    # ローカルと差分比較
    diff_files = compare_and_get_diff(box_files, local_cfg["sync_dir"])

    # 差分ファイルのみダウンロード
    download_files(diff_files, local_cfg["sync_dir"])

    # 指定アプリを起動
    exe_path = os.path.join(local_cfg["sync_dir"], local_cfg["exe_name"])
    launch_app(exe_path)

    logging.info("同期・起動完了")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"エラー発生: {e}")
        logging.error(f"エラー発生: {e}")
