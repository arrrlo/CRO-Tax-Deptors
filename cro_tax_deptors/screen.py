import click
from termcolor import cprint
from pyfiglet import figlet_format


class Screen:

    def __init__(self):
        self.data = {
            'toplist': {},
            'counters': {},
            'width': {},
            'colors': {}
        }

    def __call__(self, category, name, dept, toplist_limit, color):
        self.set_toplist(category, name, dept, toplist_limit)
        self.set_counter(category)
        self.set_color(category, color)
        self._print(toplist_limit)

    def set_toplist(self, category, name, dept, toplist_limit):
        if category not in self.data['toplist']:
            self.data['toplist'][category] = []

        self.data['toplist'][category].append((name, dept))

        sorted(self.data['toplist'][category], key=lambda deptor: deptor[1])
        if len(self.data['toplist'][category]) > toplist_limit:
            self.data['toplist'][category].pop()

        if category not in self.data['width']:
            self.data['width'][category] = 0

        for name, dept in self.data['toplist'][category]:
            w = len(name)
            if w > self.data['width'][category]:
                self.data['width'][category] = w

    def set_counter(self, category):
        if category not in self.data['counters']:
            self.data['counters'][category] = 0

        self.data['counters'][category] += 1

    def set_color(self, category, color):
        self.data['colors'][category] = color

    def _print(self, toplist_limit):
        click.clear()
        cprint(figlet_format('Croatian Tax Deptors', width=120), 'red')
        click.secho(' '*80 + 'by Ivan Arar', fg='red')

        click.echo()

        categories = self.data['counters'].keys()
        number_of_categories = len(categories)
        screen_width = sum([self.data['width'][cat]+20 for cat in self.data['width'].keys()])

        for i, category in enumerate(categories):
            cat_width = self.data['width'][category]+20
            nl = True if i+1 >= number_of_categories else False

            color = self.data['colors'][category]
            category += ' (' + str(self.data['counters'][category]) + ')'
            click.secho(category.upper() + (' '*(cat_width-len(category))), nl=nl, fg=color)

        click.echo('-'*screen_width)

        for j in range(toplist_limit):
            for i, category in enumerate(categories):

                if len(self.data['toplist'][category]) <= j:
                    break

                cat_width = self.data['width'][category]
                nl = True if i+1 >= number_of_categories else False

                color = self.data['colors'][category]
                deptor = self.data['toplist'][category][j]
                line = deptor[0] + ': ' + (' '*(cat_width-len(deptor[0]))) + deptor[1]
                click.secho(line + ' '*((cat_width+20)-len(line)), nl=nl, fg=color)

        click.echo('-'*screen_width)
        click.echo()