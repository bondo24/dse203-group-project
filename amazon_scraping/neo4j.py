from py2neo import Graph, Node, Relationship, NodeMatcher

class GraphGenerator:
    def __init__(self, config):
        config = self.validate_config(config)
        self.graph = Graph(**config)
        self.matcher = NodeMatcher(self.graph)
    
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
        # self.graph.create(amz_node)

    def create_relationships(self, acquisitions, competitors):
        if self.parent_company_node is not None:
            merged_by = Relationship.type('MergedBy')
            for company, value in acquisitions.items():
                node = self.create_company_node(company, value)
                # self.graph.create(node)
                self.graph.merge(merged_by(node, self.parent_company_node), 'company', 'title')
            compete_with = Relationship.type('CompeteWith')
            for company, value in competitors.items():
                node = self.create_company_node(company, value)
                # self.graph.create(node)
                self.graph.merge(compete_with(node, self.parent_company_node), 'company', 'title')
    def create_misc_relationships(self, relationships, name):
        # relationships should be a list containing [(source, relationship, target)]
        if relationships is not None:
            for r in relationships:
                
                print(r)
                print('\n')
                print('\n')
                print('\n')
                source = str(r[0])
                relationship = str(r[1])
                target = str(r[2])
                rel_type = Relationship.type(relationship)
                
                common_names = ['It', 'it', 'organization']

                temp_source = source
                temp_target = target
                if source in name or source in common_names:
                    temp_source = name
                if target in name or target in common_names:
                    temp_target = name

                if temp_source != temp_target:
                    source = temp_source
                    target = temp_target

                node_source = self.matcher.match('company', title=source).first()
                if node_source is None:
                    node_source = Node('entity', title=source)
                
                node_target = self.matcher.match('company', title=target).first()
                if node_target is None:
                    node_target = Node('entity', title=target)
                # self.graph.create(node_source)
                # self.graph.create(node_target)
                # should probably find a way to connect existing nodes to their correpsonding relationship
                # i.e. "Amazon is a company" should tie the "is a" relationship to the original Amazon node
                # print(self.graph.match_one(nodes=[source, target], r_type=rel_type))
                
                self.graph.merge(rel_type(node_source, node_target), 'entity', 'title')
            

    def create_company_node(self, name, company):
        return Node('company',
            title=name,
            acquired_on=company.get('acquired_on', None),
            acquired_for=company.get('acquired_for', None),
            organization=company.get('organization', None),
            founded=company.get('founded', None),
            industry=company['industry'],
            products=company['products'],
            number_of_employees=company['number_of_employees'],
            location=company.get('location', None),
            founder=company.get('founder', None),
            naics_code=company.get('naics_code', None),
            summary=company['summary'],
            )

