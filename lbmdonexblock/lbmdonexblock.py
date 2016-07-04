"""Learning By Mooc Done XBlock"""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Boolean
from xblock.fragment import Fragment
from django.utils.translation import ugettext as _


class LbmDoneXBlock(XBlock):
    """
    Shows a toggle which lets learners mark a sequence as done.
    """

    done = Boolean(
        scope = Scope.user_state,
        default = False,
        help = "Is this sequence done?"
    )

    has_score = True

    icon_class = "other"

    button_text = _("Lesson completed")

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        The primary view of the LbmDoneXBlock, shown to students
        when viewing courses.
        """

        # Load the HTML fragment from witin the package anf fill in the template
        html = self.resource_string("static/html/lbmdonexblock.html")
        frag = Fragment(html.format(self=self))

        # Load the CSS fragment
        frag.add_css(self.resource_string("static/css/lbmdonexblock.css"))

        # Load the JavaScript fragment
        frag.add_javascript(self.resource_string("static/js/src/lbmdonexblock.js"))
        frag.initialize_js('LbmDoneXBlock', {'done': self.done})

        return frag

    @XBlock.json_handler
    def toggle_button(self, data, suffix=''):
        """
        Ajax call when the button is clicked. Input is a JSON dictionary
        with one boolean field: `done`. This will save this in the
        XBlock field, and then issue an appropriate grade.
        """
        self.done = False if self.done else True
        grade = 1 if self.done else 0

        self.runtime.publish(self, 'grade', {'value': grade, 'max_value': 1})

    # Change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("LbmDoneXBlock",
             """<lbmdonexblock/>
             """),
        ]
