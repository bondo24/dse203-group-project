from py2neo import Graph, Node, Relationship

class GraphGenerator:
    def __init__(self, config):
        config = self.validate_config(config)
        self.graph = Graph(**config)
    
    def validate_config(self, config):
        if config is None:
            config = {}
        config['host'] = config.get('host', 'localhost')
        config['port'] = config.get('port', 7687)
        config['user'] = config.get('user', 'neo4j')
        config['password'] = config.get('password', 'password')
        return config

    def create_graph(self, company):
        amz_node = self.create_company_node(company['organization'], company)
        self.parent_company_node = amz_node
        self.graph.create(amz_node)

    def create_relationships(self, companies):
        if self.parent_company_node is not None:
            merged_by = Relationship.type('MergedBy')
            for company, value in companies.items():
                node = self.create_company_node(company, value)
                self.graph.create(node)
                self.graph.merge(merged_by(node, self.parent_company_node), 'company', 'title')

    def create_company_node(self, name, company):
        return Node('company',
            title=name,
            acquired_on=company.get('acquired_on', None),
            acquired_for=company.get('acquired_for', None),
            organization=company.get('organization', None),
            founded=company['founded'],
            industry=company['industry'],
            products=company['products'],
            number_of_employees=company['number_of_employees'],
            location=company['location'],
            founder=company['founder'],
            summary=company['summary'],
            )
