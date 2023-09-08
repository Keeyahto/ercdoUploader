import requests
import xml.etree.ElementTree as ET

import settings

class MyApi:
    def __init__(self):
        self.base_url = settings.HOST_NAME
        self.access_token = settings.ACCESS_TOKEN
        self.api_ping()
    def _build_headers(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/xml'
        }
        return headers

    def _send_request(self, method, endpoint, data=None):
        url = f'{self.base_url}/{endpoint}'
        headers = self._build_headers()

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, headers=headers, data=data)
            else:
                raise ValueError(f'Unsupported HTTP method: {method}')

            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            raise Exception(f'HTTP request error: {str(e)}')

    def send_get_request(self, endpoint):
        return self._send_request('GET', endpoint)

    def send_post_request(self, endpoint, payload):
        return self._send_request('POST', endpoint, data=payload)

    def parse_response(self, xml_response):
        root = ET.fromstring(xml_response)
        version = root.attrib['version']
        response_content = root.find('./response').text
        eol_date = root.attrib.get('eol', None)
        return version, response_content, eol_date

    def wrap_payload(self, payload_content, version=1):
        """
        Оборачивает PAYLOAD-CONTENT в XML-структуру в соответствии с общей структурой запроса.

        Args:
            payload_content (str): Содержимое конкретного запроса (XML-данные).
            version (str): Версия структуры отправляемого пакета данных.

        Returns:
            str: Обернутый XML-запрос.
        """
        package = ET.Element("package", version=version)
        payload = ET.Element("payload")
        payload.text = payload_content
        package.append(payload)

        xml_request = ET.tostring(package, encoding="utf-8").decode("utf-8")
        return xml_request


    def echo(self):
        endpoint = 'echo'
        response = self.send_post_request(endpoint, self.wrap_payload(''))  # Отправляем пустой POST-запрос
        return self.parse_response(response)

    def api_ping(self):
        endpoint = 'api-ping'
        response = self.send_post_request(endpoint, '')
        return self.parse_response(response)



    def set_doc_info(self, last_name, first_name, middle_name, bdate, year_completion, spec_code, spec_name, ed_level, replaced="", reason="", doc_description=None, signers=None):
        """
        Отправляет запрос set-doc-info к API.

        Args:
            last_name (str): Фамилия.
            first_name (str): Имя.
            middle_name (str): Отчество.
            bdate (str): Дата рождения.
            year_completion (str): Год выпуска.
            spec_code (str): Код специальности.
            spec_name (str): Название специальности.
            ed_level (str): Уровень образования.
            replaced (str, optional): Номер заменяемого документа.
            reason (str, optional): Причина замены.
            doc_description (list, optional): Список описаний документа.
            signers (list, optional): Список подписывающих.

        Returns:
            tuple: Возвращает кортеж с версией, содержимым ответа и датой прекращения поддержки.
        """
        # Создаем XML-запрос в соответствии с документацией
        doc_info = ET.Element("DocInfo", last_name=last_name, first_name=first_name, middle_name=middle_name, bdate=bdate, year_completion=year_completion, spec_code=spec_code, spec_name=spec_name, ed_level=ed_level)
        if replaced:
            doc_info.set("replaced", replaced)
        if reason:
            doc_info.set("reason", reason)

        if doc_description:
            for desc in doc_description:
                element = ET.Element("Element", name=desc["name"], subname=desc.get("subname", ""))
                if "header" in desc:
                    header = ET.Element("header", width=desc["header"].get("width", ""))
                    header.text = desc["header"]["text"]
                    element.append(header)
                if "value" in desc:
                    value = ET.Element("value")
                    value.text = desc["value"]
                    element.append(value)
                doc_info.append(element)

        if signers:
            for signer in signers:
                signer_element = ET.Element("Signer", code=signer["code"], id=signer["id"], role=signer["role"])
                doc_info.append(signer_element)

        payload = ET.tostring(doc_info, encoding="utf-8").decode("utf-8")
        wrapped_payload = self.wrap_payload(payload, "1")

        # Отправляем запрос
        response_content = self.send_post_request("set-doc-info", wrapped_payload)
        version, response_content, eol_date = self.parse_response(response_content)
        return version, response_content, eol_date
