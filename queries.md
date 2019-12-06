# Queries

1. Which industry do the companies belong to?
```
match (c:company)
match (n:Subclass)-[*]->(m:Root)
where n.naics_code = c.naics_code
return (c)-->(n)-[*]->(m)
```

2. What firms have been acquired/merged by the companies?

```
Match (c:company)-[:`have acquire`| acquire| MergedBy]->(n)
return c,n
```

3. What did the companies launch?
```
Match (c:company)-[r:launch]->(e:entity) return c,e
```

4. Where have the companies expanded?
```
Match (c:company)-[r:`have expand`|expand]->(e)
return c,e
```

5. What business did the companies open or will open?
```
Match (c:company)-[:open |:`will open`]->(e:entity)
return c,e
```

6. What have the companies hosted?
```
match (c)-[:`would be host`|:`have host`]-(n)
return c,n
```

7. What situations have the companies faced?
```
Match (c:company)-[:`have face`| face]->(n)
return c,n
```

8. Identify the companies in the same industry.
```
match (n:company)
with n.naics_code as prop, collect(n) as
nodelist, count(*) as count
where count > 1
return nodelist
```

9. What companies are competing with Amazon’s competitors?
```
Match (c:company)-[r:CompeteWith | compete]->(e)
where c.title in ['Netflix','FedEx', 'Etsy']
return c,e
```

10. Did Amazon’s competitors win/earn any recognitions/awards ?
```
Match (c:company)-[r:earn| win]->(e) where c.title in
['Netflix','FedEx', 'Etsy'] return c,e
```

11. What is the other extracted interesting information for Amazon?
```
Match (c:company{title:'Amazon.com, Inc.'})-[r:`would comanage`| oppose | `would be acquire`| grow |`would buy` | surpass | `would be acquiring`]->(e:entity) return c,e
```
