def get_chart_config(data):
    """Generate chart configurations for all charts"""
    main_chart = {
        'type': 'line',
        'data': {
            'labels': data['labels'].reverse(),
            'datasets': [
                {
                    'label': 'Price',
                    'data': data['prices'].reverse(),
                    'borderColor': '#2c3e50',
                    'tension': 0.1
                },
                {
                    'label': '20-day MA',
                    'data': ([None] * (len(data['labels']) - len(data['ma20']))) + data['ma20'].reverse(),
                    'borderColor': '#e74c3c',
                    'borderWidth': 1,
                    'pointRadius': 0
                },
                {
                    'label': '50-day MA',
                    'data': ([None] * (len(data['labels']) - len(data['ma50']))) + data['ma50'].reverse(),
                    'borderColor': '#3498db',
                    'borderWidth': 1,
                    'pointRadius': 0
                }
            ]
        },
        'options': {
            'responsive': True,
            'maintainAspectRatio': False,
            'plugins': {
                'legend': {
                    'position': 'top'
                },
                'annotation': {
                    'annotations': {}
                }
            },
            'scales': {
                'y': {
                    'beginAtZero': False
                }
            }
        }
    }

    rsi_chart = {
        'type': 'line',
        'data': {
            'labels': data['labels'],
            'datasets': [{
                'label': 'RSI',
                'data': data['indicators']['rsi'].reverse(),
                'borderColor': '#8e44ad',
                'borderWidth': 1
            }]
        },
        'options': {
            'responsive': True,
            'maintainAspectRatio': False,
            'plugins': {
                'annotation': {
                    'annotations': {
                        'overbought': {
                            'type': 'line',
                            'yMin': 70,
                            'yMax': 70,
                            'borderColor': '#e74c3c',
                            'borderWidth': 1,
                            'borderDash': [5, 5]
                        },
                        'oversold': {
                            'type': 'line',
                            'yMin': 30,
                            'yMax': 30,
                            'borderColor': '#2ecc71',
                            'borderWidth': 1,
                            'borderDash': [5, 5]
                        }
                    }
                }
            },
            'scales': {
                'y': {
                    'min': 0,
                    'max': 100
                }
            }
        }
    }

    macd_chart = {
        'type': 'bar',
        'data': {
            'labels': data['labels'],
            'datasets': [
                {
                    'label': 'MACD',
                    'data': data['indicators']['macd']['macd'].reverse(),
                    'type': 'line',
                    'borderColor': '#2980b9',
                    'fill': False
                },
                {
                    'label': 'Signal',
                    'data': data['indicators']['macd']['signal'].reverse(),
                    'type': 'line',
                    'borderColor': '#e67e22',
                    'fill': False
                },
                {
                    'label': 'Histogram',
                    'data': data['indicators']['macd']['histogram'].reverse(),
                    'backgroundColor': '#2ecc71',
                    'backgroundColor': 'function(context) { return context.raw >= 0 ? "#2ecc71" : "#e74c3c"; }'
                }
            ]
        },
        'options': {
            'responsive': True,
            'maintainAspectRatio': False
        }
    }

    # Add SMC markers if available
    if 'smc_markers' in data:
        annotations = main_chart['options']['plugins']['annotation']['annotations']
        
        # Add imbalance points
        for i, imb in enumerate(data['smc_markers']['imbalances']):
            annotations[f'imbalance{i}'] = {
                'type': 'point',
                'xValue': len(data['labels']) - 1 - imb['index'],
                'yValue': imb['price'],
                'backgroundColor': '#27ae60' if imb['type'] == 'bullish' else '#c0392b',
                'radius': 6 * imb['strength'],
                'borderColor': 'white',
                'borderWidth': 2
            }
        
        # Add liquidity levels
        for i, level in enumerate(data['smc_markers']['liquidity_levels']):
            annotations[f'liquidity{i}'] = {
                'type': 'line',
                'yMin': level['price'],
                'yMax': level['price'],
                'borderColor': '#2ecc71' if level['type'] == 'support' else '#e74c3c',
                'borderWidth': 2 * level['strength'],
                'borderDash': [5, 5]
            }
        
        # Add FVG boxes
        for i, fvg in enumerate(data['smc_markers']['fvgs']):
            annotations[f'fvg{i}'] = {
                'type': 'box',
                'xMin': len(data['labels']) - 1 - fvg['index'] - 0.5,
                'xMax': len(data['labels']) - 1 - fvg['index'] + 0.5,
                'yMin': fvg['price'] - fvg['gap_size'],
                'yMax': fvg['price'] + fvg['gap_size'],
                'backgroundColor': f'rgba({39 if fvg["type"] == "bullish" else 192}, {174 if fvg["type"] == "bullish" else 57}, {96 if fvg["type"] == "bullish" else 43}, 0.2)',
                'borderColor': '#27ae60' if fvg['type'] == 'bullish' else '#c0392b',
                'borderWidth': 1
            }
    
    return {
        'main': main_chart,
        'rsi': rsi_chart,
        'macd': macd_chart
    }