import random
from typing import List, Dict, Any

class AISuggester:
    def __init__(self):
        self.furniture_categories = {
            'seating': ['sofa', 'chair', 'armchair', 'bench', 'ottoman'],
            'tables': ['coffee_table', 'dining_table', 'side_table', 'desk'],
            'storage': ['bookshelf', 'cabinet', 'dresser', 'wardrobe'],
            'lighting': ['floor_lamp', 'table_lamp', 'ceiling_light', 'pendant_light'],
            'decor': ['plant', 'artwork', 'mirror', 'rug']
        }
        
        self.color_palettes = {
            'modern': {
                'primary': ['#2563EB', '#7C3AED', '#059669', '#DC2626'],
                'neutral': ['#374151', '#6B7280', '#9CA3AF', '#D1D5DB'],
                'accent': ['#F59E0B', '#EF4444', '#10B981', '#8B5CF6']
            },
            'traditional': {
                'primary': ['#92400E', '#7C2D12', '#065F46', '#1E40AF'],
                'neutral': ['#78716C', '#A8A29E', '#D6D3D1', '#F5F5F4'],
                'accent': ['#DC2626', '#059669', '#7C3AED', '#EA580C']
            },
            'minimalist': {
                'primary': ['#FFFFFF', '#F8FAFC', '#E2E8F0', '#CBD5E1'],
                'neutral': ['#64748B', '#475569', '#334155', '#1E293B'],
                'accent': ['#0F172A', '#EF4444', '#3B82F6', '#10B981']
            }
        }
    
    def analyze_current_furniture(self, placed_models: List[Dict]) -> Dict[str, Any]:
        """Analyze the current furniture setup and return insights."""
        analysis = {
            'total_items': len(placed_models),
            'categories': {},
            'style_hints': [],
            'missing_essentials': [],
            'color_analysis': []
        }
        
        # Count items by category
        for model in placed_models:
            name = model.get('name', '').lower()
            category = self._categorize_furniture(name)
            analysis['categories'][category] = analysis['categories'].get(category, 0) + 1
        
        # Identify missing essentials for common rooms
        analysis['missing_essentials'] = self._identify_missing_essentials(analysis['categories'])
        
        # Generate style hints
        analysis['style_hints'] = self._generate_style_hints(placed_models)
        
        return analysis
    
    def _categorize_furniture(self, item_name: str) -> str:
        """Categorize furniture item based on its name."""
        for category, items in self.furniture_categories.items():
            for item in items:
                if item.replace('_', ' ') in item_name or item_name in item:
                    return category
        return 'other'
    
    def _identify_missing_essentials(self, categories: Dict[str, int]) -> List[str]:
        """Identify missing essential furniture items."""
        missing = []
        
        if categories.get('seating', 0) == 0:
            missing.append('seating')
        if categories.get('tables', 0) == 0:
            missing.append('tables')
        if categories.get('lighting', 0) == 0:
            missing.append('lighting')
        
        return missing
    
    def _generate_style_hints(self, placed_models: List[Dict]) -> List[str]:
        """Generate style hints based on placed models."""
        hints = []
        
        # Simple heuristics based on model names
        model_names = [model.get('name', '').lower() for model in placed_models]
        
        if any('modern' in name for name in model_names):
            hints.append('modern')
        if any('traditional' in name or 'classic' in name for name in model_names):
            hints.append('traditional')
        if any('minimal' in name for name in model_names):
            hints.append('minimalist')
        
        return hints if hints else ['modern']  # Default to modern
    
    def generate_full_suggestions(self, placed_models: List[Dict], db=None) -> Dict[str, Any]:
        """Generate comprehensive AI suggestions for the room."""
        analysis = self.analyze_current_furniture(placed_models)
        
        suggestions = {
            'furniture_suggestions': [],
            'color_suggestions': [],
            'layout_suggestions': [],
            'style_recommendations': [],
            'analysis': analysis,
            'suggested_models': []  # New: specific model recommendations
        }
        
        # Generate furniture suggestions based on missing items
        for missing_category in analysis['missing_essentials']:
            category_items = self.furniture_categories.get(missing_category, [])
            if category_items:
                suggested_item = random.choice(category_items)
                suggestion = {
                    'category': missing_category,
                    'item': suggested_item,
                    'reason': f'Your room would benefit from {missing_category.replace("_", " ")}'
                }
                suggestions['furniture_suggestions'].append(suggestion)
                
                # Try to find actual models from database
                if db is not None:
                    try:
                        models_collection = db['model3ds']
                        # Search for models matching the suggested item
                        # Your database uses format like "furniture-seating", "furniture-tables", etc.
                        category_search = f'furniture-{missing_category}' if missing_category != 'decor' else 'furniture-decor'
                        
                        query = {
                            '$or': [
                                {'name': {'$regex': suggested_item.replace('_', ' '), '$options': 'i'}},
                                {'category': {'$regex': category_search, '$options': 'i'}},
                                {'subcategory': {'$regex': suggested_item.replace('_', ' '), '$options': 'i'}},
                                {'tags': {'$in': [suggested_item.replace('_', ' '), missing_category]}}
                            ]
                        }
                        print(f'🔍 Searching for models with query: {query}')
                        matching_models = list(models_collection.find(query).limit(3))
                        print(f'✅ Found {len(matching_models)} matching models for category: {missing_category}')
                        
                        for model in matching_models:
                            model_suggestion = {
                                '_id': str(model['_id']),
                                'name': model.get('name', ''),
                                'category': model.get('category', ''),
                                'thumbnailUrl': model.get('thumbnailUrl', ''),
                                'fileUrl': model.get('fileUrl', ''),
                                'reason': f'Recommended {missing_category.replace("_", " ")} to complete your design'
                            }
                            suggestions['suggested_models'].append(model_suggestion)
                            print(f'  📦 Added model: {model.get("name", "Unnamed")}')
                    except Exception as e:
                        print(f'❌ Error fetching models from database: {e}')
                        import traceback
                        traceback.print_exc()
                else:
                    print(f'⚠️  Database is None, cannot fetch models')
        
        # Generate color suggestions
        style = analysis['style_hints'][0] if analysis['style_hints'] else 'modern'
        palette = self.color_palettes.get(style, self.color_palettes['modern'])
        
        color_suggestions = [
            {
                'color': random.choice(palette['primary']),
                'type': 'primary',
                'description': f'Primary {style} color for main furniture pieces'
            },
            {
                'color': random.choice(palette['accent']),
                'type': 'accent',
                'description': f'Accent color for decorative elements'
            },
            {
                'color': random.choice(palette['neutral']),
                'type': 'neutral',
                'description': f'Neutral {style} color for walls and backgrounds'
            }
        ]
        
        # Add more color suggestions based on the number of furniture items
        if analysis['total_items'] > 2:
            color_suggestions.append({
                'color': random.choice(palette['primary']),
                'type': 'secondary',
                'description': f'Secondary color to complement your {style} theme'
            })
            
        if analysis['total_items'] > 4:
            color_suggestions.append({
                'color': random.choice(palette['accent']),
                'type': 'highlight',
                'description': f'Highlight color for special decorative pieces'
            })
            
        suggestions['color_suggestions'] = color_suggestions
        
        # Generate layout suggestions
        suggestions['layout_suggestions'] = self._generate_layout_suggestions(analysis)
        
        # Style recommendations
        suggestions['style_recommendations'] = [
            f'Based on your current setup, consider {style} style elements',
            'Add some plants for a natural touch',
            'Consider adding artwork to personalize the space'
        ]
        
        # Log summary
        print(f'📊 AI Suggestions Summary:')
        print(f'  - Furniture suggestions: {len(suggestions["furniture_suggestions"])}')
        print(f'  - Suggested models from DB: {len(suggestions["suggested_models"])}')
        print(f'  - Color suggestions: {len(suggestions["color_suggestions"])}')
        
        return suggestions
    
    def _generate_layout_suggestions(self, analysis: Dict) -> List[str]:
        """Generate layout suggestions based on furniture analysis."""
        suggestions = []
        
        if analysis['categories'].get('seating', 0) > 0 and analysis['categories'].get('tables', 0) == 0:
            suggestions.append('Add a coffee table to complement your seating area')
        
        if analysis['categories'].get('lighting', 0) == 0:
            suggestions.append('Add lighting to create ambiance and functionality')
        
        if analysis['total_items'] < 3:
            suggestions.append('Consider adding more furniture to create a complete room')
        
        return suggestions
    
    def suggest_colors(self, analysis: Dict, furniture_type: str) -> Dict[str, Any]:
        """Suggest colors for a specific furniture type."""
        style = analysis['style_hints'][0] if analysis['style_hints'] else 'modern'
        palette = self.color_palettes.get(style, self.color_palettes['modern'])
        
        # Choose appropriate color based on furniture type
        if furniture_type in ['sofa', 'chair', 'armchair']:
            # Main seating can use primary or neutral colors
            color_options = palette['primary'] + palette['neutral']
        elif furniture_type in ['coffee_table', 'dining_table', 'desk']:
            # Tables usually neutral or natural
            color_options = palette['neutral']
        else:
            # Other items can use accent colors
            color_options = palette['accent'] + palette['neutral']
        
        primary_color = random.choice(color_options)
        
        return {
            'primary_color': primary_color,
            'complementary_colors': random.sample(palette['accent'], 2),
            'style': style,
            'reasoning': f'This {primary_color} works well for {furniture_type} in {style} style',
            'confidence': random.uniform(0.8, 0.95)
        }

# Create global instance
ai_suggester = AISuggester()
