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

    def create_graph(self, company=None):
        # hard coding amazon for now
        amz_node = Node('company', title='Amazon')
        self.parent_company_node = amz_node
        self.graph.create(amz_node)

    def create_relationships(self, companies):
        if self.parent_company_node is not None:
            merged_by = Relationship.type('MergedBy')
            for company, value in companies.items():
                node = Node('company',
                            title=company,
                            acquired_on=value['acquired_on'],
                            acquired_for=value['acquired_for'],
                            organization=value['organization'],
                            founded=value['founded'],
                            industry=value['industry'],
                            products=value['products'],
                            number_of_employees=value['number_of_employees'],
                            location=value['location'],
                            founder=value['founder'],
                            summary=value['summary'],
                            )
                self.graph.create(node)
                self.graph.merge(merged_by(node, self.parent_company_node), 'company', 'title')
