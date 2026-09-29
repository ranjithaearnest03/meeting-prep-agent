import unittest
import json
from app import app
from database import init_db
from samples import SAMPLES

class TestMeetingPrepAgent(unittest.TestCase):
    def setUp(self):
        init_db()
        self.client = app.test_client()

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Meeting Prep Agent', response.data)
        self.assertIn(b'Prepare Meeting', response.data)

    def test_samples_endpoints(self):
        # List all samples
        response = self.client.get('/api/samples')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertGreaterEqual(len(data['samples']), 4)

        # Get specific sample
        first_sample_id = data['samples'][0]['id']
        resp2 = self.client.get(f'/api/samples/{first_sample_id}')
        self.assertEqual(resp2.status_code, 200)
        sample_data = resp2.get_json()
        self.assertTrue(sample_data['success'])
        self.assertEqual(sample_data['sample']['id'], first_sample_id)

    def test_all_sample_scenarios_generate_briefs(self):
        for sample in SAMPLES:
            payload = {
                "title": sample["title"],
                "person_company": sample["person_company"],
                "date_time": sample["date_time"],
                "purpose": sample["purpose"],
                "previous_notes": sample["previous_notes"],
                "additional_info": sample["additional_info"],
                "save_history": True
            }
            response = self.client.post('/api/prepare-meeting', json=payload)
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertTrue(data['success'])
            brief = data['brief']

            # Verify all 7 required sections are present and non-empty
            self.assertIn('meeting_objective', brief)
            self.assertTrue(brief['meeting_objective']['primary'])
            self.assertGreaterEqual(len(brief['meeting_objective']['success_criteria']), 1)

            self.assertIn('person_company_summary', brief)
            self.assertTrue(len(brief['person_company_summary']) > 10)

            self.assertIn('key_discussion_points', brief)
            self.assertGreaterEqual(len(brief['key_discussion_points']), 3)

            self.assertIn('important_questions', brief)
            self.assertGreaterEqual(len(brief['important_questions']), 3)

            self.assertIn('suggested_talking_points', brief)
            self.assertGreaterEqual(len(brief['suggested_talking_points']), 2)

            self.assertIn('possible_concerns_objections', brief)
            self.assertGreaterEqual(len(brief['possible_concerns_objections']), 1)

            self.assertIn('recommended_next_steps', brief)
            self.assertGreaterEqual(len(brief['recommended_next_steps']), 2)

    def test_validation_missing_fields(self):
        # Missing title
        resp1 = self.client.post('/api/prepare-meeting', json={"title": "", "person_company": "Acme"})
        self.assertEqual(resp1.status_code, 400)
        
        # Missing person/company
        resp2 = self.client.post('/api/prepare-meeting', json={"title": "Demo", "person_company": ""})
        self.assertEqual(resp2.status_code, 400)

    def test_meeting_lifecycle_save_get_delete(self):
        # Create meeting
        payload = {
            "title": "Quarterly Strategy Review",
            "person_company": "Beta Corp",
            "date_time": "Next Monday 10:00 AM",
            "purpose": "Define OKRs for Q4",
            "previous_notes": "Completed Q3 targets on time",
            "additional_info": "Focus on mobile app growth",
            "save_history": True
        }
        res_create = self.client.post('/api/prepare-meeting', json=payload)
        self.assertEqual(res_create.status_code, 200)
        meeting_id = res_create.get_json()['meeting_id']
        self.assertIsNotNone(meeting_id)

        # Get meeting by ID
        res_get = self.client.get(f'/api/meetings/{meeting_id}')
        self.assertEqual(res_get.status_code, 200)
        m = res_get.get_json()['meeting']
        self.assertEqual(m['title'], "Quarterly Strategy Review")
        self.assertIn('brief', m)

        # Delete meeting
        res_del = self.client.delete(f'/api/meetings/{meeting_id}')
        self.assertEqual(res_del.status_code, 200)

        # Verify not found after deletion
        res_get2 = self.client.get(f'/api/meetings/{meeting_id}')
        self.assertEqual(res_get2.status_code, 404)

if __name__ == '__main__':
    unittest.main()
