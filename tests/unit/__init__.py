import os
import sys

# テスト対象を呼び出せるようにするため、ソースコードの配置場所をimportする。
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../../src/"))
# moto（boto3のモック）を呼び出すときにリージョンを省略したい場合には、環境変数でデフォルトのリージョンを指定しておいたほうが無難です。
os.environ['AWS_DEFAULT_REGION'] = 'ap-northeast-1'
