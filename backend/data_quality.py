import re
from validate_docbr import CPF, CNPJ  # Biblioteca para validação de documentos
from email_validator import validate_email, EmailNotValidError

class DataQuality:
    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        """Valida CPF usando a biblioteca validate_docbr."""
        print(f"Validando CPF recebido: '{cpf}'") 
        cpf = ''.join(filter(str.isdigit, cpf))  # Remove caracteres não numéricos
        print(f"CPF após limpeza: '{cpf}'")
        return CPF().validate(cpf)
    
    '''
    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
            
        # Cálculo dos dígitos verificadores
        for i in range(9, 11):
            value = sum((int(cpf[num]) * ((i+1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != int(cpf[i]):
                return False
        return True
    '''

    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida e-mail com a biblioteca email-validator."""
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False
        
    @staticmethod
    def normalize_cpf(cpf: str) -> str:
        return ''.join(filter(str.isdigit, cpf))
    
    '''
    @staticmethod
    def format_cpf(cpf: str) -> str:
        """Formata CPF para o padrão XXX.XXX.XXX-XX."""
        cpf = ''.join(filter(str.isdigit, cpf))
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"
    '''

    @staticmethod
    def anonymize_data(text: str, keep_last_chars: int = 2) -> str:
        """Anonimiza dados sensíveis (ex: '123.456.789-00' → '***.***.***-00')."""
        if not text:
            return text
        visible_part = text[-keep_last_chars:]
        return f"{'*' * (len(text) - keep_last_chars)}{visible_part}"

    @staticmethod
    def normalize_name(name: str) -> str:
        """Padroniza nomes (capitaliza e remove espaços extras)."""
        return ' '.join(word.capitalize() for word in name.split() if word.strip())

    @staticmethod
    def is_pii_field(field_name: str) -> bool:
        """Identifica se um campo contém PII (Informação Pessoal Identificável)."""
        pii_keywords = ["cpf", "email", "nome", "endereço", "telefone"]
        return any(keyword in field_name.lower() for keyword in pii_keywords)

#print(DataQuality.validate_cpf("529.982.247-26"))  # Deve retornar True
#print(DataQuality.normalize_cpf("529.982.247-25"))  # Deve retornar "52998224725"