import shutil
from datetime import datetime

backup_dir = 'backup/'
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_file = f'{backup_dir}variables_backup_{timestamp}.json'

shutil.copy2('variables.json', backup_file)
