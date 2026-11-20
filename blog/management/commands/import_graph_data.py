from django.core.management.base import BaseCommand
from blog.models import GraphNode, GraphEdge
import json
import os


class Command(BaseCommand):
    help = 'Import knowledge graph data from JSON file'

    def handle(self, *args, **options):
        # Path to the JSON file
        json_path = os.path.join('static', 'js', 'knowledge-graph-data.json')
        
        self.stdout.write(f'Loading data from {json_path}...')
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Import nodes
        self.stdout.write('Importing nodes...')
        nodes_created = 0
        nodes_updated = 0
        
        for node_data in data['nodes']:
            node, created = GraphNode.objects.update_or_create(
                node_id=node_data['id'],
                defaults={
                    'label': node_data['label'],
                    'kind': node_data['kind'],
                    'day': node_data.get('day'),
                    'week': node_data['week'],
                    'summary': node_data['summary'],
                    'example': node_data.get('example', ''),
                }
            )
            if created:
                nodes_created += 1
            else:
                nodes_updated += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'Nodes: {nodes_created} created, {nodes_updated} updated'
        ))
        
        # Import edges
        self.stdout.write('Importing edges...')
        edges_created = 0
        edges_updated = 0
        
        for edge_data in data['edges']:
            source = GraphNode.objects.get(node_id=edge_data['source'])
            target = GraphNode.objects.get(node_id=edge_data['target'])
            
            edge, created = GraphEdge.objects.update_or_create(
                source=source,
                target=target,
                relation=edge_data['relation'],
                defaults={
                    'basis': edge_data['basis'],
                }
            )
            if created:
                edges_created += 1
            else:
                edges_updated += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'Edges: {edges_created} created, {edges_updated} updated'
        ))
        
        self.stdout.write(self.style.SUCCESS('Import complete!'))
