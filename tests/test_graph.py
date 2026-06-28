import unittest
from unittest.mock import patch
from langgraph_reflection import build_graph

class TestGraph(unittest.TestCase):
    @patch('langgraph_reflection.ChatOpenAI')
    def test_reflection_flow(self, MockChat):
        instance = MockChat.return_value
        instance.invoke.side_effect = [
            "Draft answer 1",
            '{"verdict":"needs_revision","critique":"Point 1\\nPoint 2"}',
            "Rewritten answer",
            '{"verdict":"ok","critique":"All good"}'
        ]
        graph = build_graph()
        state = {
            "question": "Test question",
            "draft": "",
            "critique": "",
            "verdict": "",
            "round": 1,
            "max_rounds": 2
        }
        final_state = graph.invoke(state)
        self.assertEqual(final_state["draft"], "Rewritten answer")
        self.assertEqual(final_state["verdict"], "ok")
        self.assertEqual(final_state["round"], 2)

if __name__ == "__main__":
    unittest.main()
