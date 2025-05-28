class Group:
    def __init__(self,
                 group_id,
                 name,
                 subject_owner,
                 subject_time,
                 picture_url,
                 size,
                 creation,
                 owner,
                 restrict,
                 announce,
                 is_community,
                 is_community_announce,
                 dias =1,
                 horario="22:00",
                 enabled=False,
                 is_links=False,
                 is_names=False
                 ):
        """
        Args:
            gruoup_id (_type_): ID do group
            name (_type_): nome do grupo
            subject_owner (_type_): Dono do assunto ou titulo do group
            subject_time (_type_): timestamtp da ultima alteracao
            picture_url (_type_): imagem do group
            size (_type_): numero de participantes
            creation (_type_): timestamp de criacao
            owner (_type_): dono
            restrict (_type_): restricoes no grupo?
            announce (_type_): modo somente administrador
            is_community (bool): _description_
            is_community_announce (bool): anuncio de uma comunidade?
            dias (int, optional): quantidade de dias para resumo. Defaults to 1.
            horario (str, optional): horario de execucao de resumo. Defaults to "22:00".
            enabled (bool, optional): resumo habilitado?. Defaults to False.
            is_links (bool, optional): Links incluidos no resumo. Defaults to False.
            is_names (bool, optional): nomes incluidos no resumo. Defaults to False.
        """
        self.group_id = group_id
        self.name = name
        self.subject_owner = subject_owner
        self.subject_time = subject_time
        self.picture_url = picture_url
        self.size = size
        self.creation= creation
        self.owner = owner
        self.restrict = restrict
        self.announce = announce
        self.is_community = is_community
        self.is_community_announce = is_community_announce
        
        #config de resumo:
        self.dias = dias
        self.horario = horario
        self.enabled = enabled
        self.is_links = is_links
        self.is_names = is_names
    
    def __repr__(self):
        """Retorna uma representacao legivel do group"""
        
        return(
            f"Group(id={self.group_id},name={self.name},owner={self.owner}, size={self.size})"
        )
        
        