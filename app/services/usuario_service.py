from app.models.usuario import Usuario
from app.extensions import db

class UsuarioService:
    def criar_usuario(self, data:dict) -> Usuario:
        cpf = data.get("cpf", "")
        if not cpf or len(cpf) != 11:
            raise ValueError("CPF Inválido")
        
        usuario = Usuario.query.get(data["cpf"])
        if usuario:
            raise ValueError("Usuário já cadastrado")
        
        usuario = Usuario(**data)
        db.session.add(usuario)
        db.session.commit()

        return usuario

    def listar_usuarios(self):
        return Usuario.query.all()
    
    def obter_usuario(self, cpf: str) -> Usuario:
        usuario = Usuario.query.get(cpf)
        if not usuario:
            raise ValueError("Usuario não encontrado")
        
        return usuario
    
    def obter_nome_usuario_por_cpf(self, cpf):
        usuario = Usuario.query.get(cpf)
        if not usuario:
            raise ValueError("Usuario não encontrado")
        
        return usuario.nome
    
    def atualiza_cadastro_usuario(self, cpf: str, data: dict) -> Usuario:
        usuario = Usuario.query.get(cpf)
        if not usuario:
            raise ValueError("Usuario não encontrado")
        
        if "nome" in data:
            if data["nome"] is None:
                raise ValueError("Nome não pode ser vazio")
            usuario.nome = data["nome"]

        if "email" in data:
            usuario.email = data["email"]

        if "data_nascimento" in data:
            usuario.data_nascimento = data["data_nascimento"]

        db.session.commit()
        return usuario

    def excluir_usuario(self, cpf:str) -> None:
        usuario = Usuario.query.get(cpf)
        if not usuario:
            raise ValueError("Usuario não encontrado")
        
        db.session.delete(usuario)
        db.session.commit()
