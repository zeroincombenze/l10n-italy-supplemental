import odoo.tests
# Part of Odoo. See LICENSE file for full copyright and licensing details.


@odoo.tests.tagged('post_install', '-at_install')
class TestAgentUi(odoo.tests.HttpCase):

    def test_01_agent_tour(self):
        self.start_tour("/web", 'Agent_Tour', login="admin", step_delay=100)
