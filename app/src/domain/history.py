from mongo_models import ClickHistoryModel


def write(history_id, data, index):
    event = {'decision_index': index, 'user_opts': []}
    for answer in data.get('button_rows', []):
        event['user_opts'].append({'title': answer.get('title'),
                                   'answers': [a.get('label') for a in answer.get('answers') if a.get('active')],
                                   'id': answer.get('id')})
    for entry in data.get('numeric_rows', []):
        event['user_opts'].append({'title': entry.get('title'), 'values': entry.get('values'), 'id': entry.get('id')})

    for key in ['meetings', 'tasks_total', 'tasks_done', 'cost', 'current_day', 'actual_cost', 'motivation',
                'familiarity', 'stress']:
        if (value := data.get(key)) is not None:
            event[key] = value
    _write(event, history_id)


def _write(event, id):
    model = ClickHistoryModel()
    model.add_event(id, event)
