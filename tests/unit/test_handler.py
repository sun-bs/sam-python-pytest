import src.app as app
import src
import pytest
import json
import src.custom_exception as custom_exception


# テストクラスは「Test」から始まる命名としないとテストクラスとして認識されません。
class TestApp:
    # テストメソッドは「test_」から始まる命名としないとテストクラスとして認識されません。
    def test_success(self):
        """
        何もモックしない
        """
        rtn = app.lambda_handler({'requestContext': {'resourcePath': 'success'}}, None)
        assert json.loads(rtn['body'])['message'] == 'dummyMessage'

    def test_success_with_mock(self, mocker):
        """
        return_valueをモックして戻り値を変更する
        """
        mock = mocker.patch('src.app.return_value', return_value='mockMessage')
        rtn = app.lambda_handler({'requestContext': {'resourcePath': 'dummyPath'}}, None)
        # 戻り値を検証
        assert rtn['statusCode'] is 200
        assert json.loads(rtn['body'])['message'] == 'mockMessage'
        # モックが呼び出された回数を検証
        assert mock.call_count == 1

    def test_bad_request_with_mock(self, mocker, caplog):
        """
        return_valueをモックしてカスタム例外（CustomException）を発生させる。
        """
        # モック対象と戻り値をsrc.app配下の絶対パスで指定します。
        # モック対象と戻り値をテストモジュール内（このファイル）でimportとしてそのパスを指定しても意図した動作となりません。
        mock = mocker.patch('src.app.return_value', side_effect=src.app.CustomException())
        rtn = app.lambda_handler({'requestContext': {'resourcePath': 'dummyPath'}}, None)
        # 戻り値を検証
        assert rtn['statusCode'] == 400
        assert json.loads(rtn['body'])['message'] == 'bad request'
        # loggerによって出力されたのログを検証。
        assert 'CustomExceptionをキャッチ' in caplog.text
        # モックが呼び出された回数を検証
        assert mock.call_count == 1

    def test_bad_request_with_mock_uncatched_exception(self, mocker, caplog):
        """
        return_valueをモックしてカスタム例外（UncatchedException）を発生させる。
        """
        # 戻り値にapp内でimportしていない例外を指定する場合、前段のようにsrc.app配下のパスを指定できません。
        # テストモジュール内（このファイル）でimportした例外を指定します。
        # （app.pyではExceptionをcatchしているので、テストモジュール内でimportした例外であってもキャッチされます。）
        mock = mocker.patch('src.app.return_value', side_effect=custom_exception.UncatchedException())
        with pytest.raises(Exception) as e:
            app.lambda_handler({'requestContext': {'resourcePath': 'dummyPath'}}, None)
        assert e.type == custom_exception.UncatchedException
        # loggerによって出力されたのログを検証
        assert 'UncatchedExceptionをキャッチ' in caplog.text
        # モックが呼び出された回数を検証
        assert mock.call_count == 1
