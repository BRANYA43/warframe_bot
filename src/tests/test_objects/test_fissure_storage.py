import unittest
from datetime import datetime, timedelta
from uuid import uuid4

import data
from objects import FissureStorage, Fissure


class TestFissureStorage(unittest.TestCase):
    """Test FissureStorage"""

    def setUp(self) -> None:
        self.storage = FissureStorage()
        self.data = {
            'id': 'some_id',
            'name': 'name',
            'location': data.LOCATIONS[0],
            'type': data.TYPES[0],
            'enemy': data.ENEMIES[0],
            'tier': data.TIERS[0],
            'expiry': datetime.utcnow() + timedelta(days=1)
        }

    def fill_storage(self):
        for tier in data.TIERS[:-1]:
            self.data['tier'] = tier
            self.data['id'] = str(uuid4())
            self.storage.add(Fissure(**self.data))
            self.data['id'] = str(uuid4())
            self.storage.add(Fissure(**self.data, is_storm=True))
            self.data['id'] = str(uuid4())
            self.storage.add(Fissure(**self.data, is_hard=True))

        self.data['tier'] = data.TIERS[-1]
        self.data['location'] = data.LOCATIONS[-8]
        self.data['id'] = str(uuid4())
        self.storage.add(Fissure(**self.data))

    def test_fissure_storage_has_needed_attrs(self):
        self.assertIsInstance(self.storage._simple_fissures, dict)
        self.assertIsInstance(self.storage._storm_fissures, dict)
        self.assertIsInstance(self.storage._hard_fissures, dict)
        self.assertIsInstance(self.storage._kuva_fissures, list)
        for tier in ('lith', 'meso', 'neo', 'axi'):
            self.assertIn(tier, self.storage._simple_fissures.keys())
            self.assertIn(tier, self.storage._storm_fissures.keys())
            self.assertIn(tier, self.storage._hard_fissures.keys())

    def test_add_to_simple_with_lith_tier(self):
        """Test: add fissure to simple fissures with lith tier."""
        fissure = Fissure(**self.data)

        self.assertEqual(len(self.storage._simple_fissures['lith']), 0)

        self.storage.add(fissure)

        self.assertEqual(len(self.storage._simple_fissures['lith']), 1)

    def test_add_to_simple_with_meso_tier(self):
        """Test: add fissure to simple fissures with meso tier."""
        self.data['tier'] = data.TIERS[1]
        fissure = Fissure(**self.data)

        self.assertEqual(len(self.storage._simple_fissures['meso']), 0)

        self.storage.add(fissure)

        self.assertEqual(len(self.storage._simple_fissures['meso']), 1)

    def test_add_to_simple_with_neo_tier(self):
        """Test: add fissure to simple fissures with neo tier."""
        self.data['tier'] = data.TIERS[2]
        fissure = Fissure(**self.data)

        self.assertEqual(len(self.storage._simple_fissures['neo']), 0)

        self.storage.add(fissure)

        self.assertEqual(len(self.storage._simple_fissures['neo']), 1)

    def test_add_to_simple_with_axi_tier(self):
        """Test: add fissure to simple fissures with axi tier."""
        self.data['tier'] = data.TIERS[3]
        fissure = Fissure(**self.data)

        self.assertEqual(len(self.storage._simple_fissures['axi']), 0)

        self.storage.add(fissure)

        self.assertEqual(len(self.storage._simple_fissures['axi']), 1)

    def test_add_to_storm_with_lith_tier(self):
        """Test: add fissure to storm fissures with lith tier."""
        self.data['is_storm'] = True
        fissure = Fissure(**self.data)

        self.assertEqual(len(self.storage._storm_fissures['lith']), 0)

        self.storage.add(fissure)

        self.assertEqual(len(self.storage._storm_fissures['lith']), 1)

    def test_add_to_storm_with_meso_tier(self):
        """Test: add fissure to storm fissures with meso tier."""
        self.data['is_storm'] = True
        self.data['tier'] = data.TIERS[1]
        fissure = Fissure(**self.data)

        self.assertEqual(len(self.storage._storm_fissures['meso']), 0)

        self.storage.add(fissure)

        self.assertEqual(len(self.storage._storm_fissures['meso']), 1)

    def test_add_to_storm_with_neo_tier(self):
        """Test: add fissure to storm fissures with neo tier."""
        self.data['is_storm'] = True
        self.data['tier'] = data.TIERS[2]
        fissure = Fissure(**self.data)

        self.assertEqual(len(self.storage._storm_fissures['neo']), 0)

        self.storage.add(fissure)

        self.assertEqual(len(self.storage._storm_fissures['neo']), 1)

    def test_add_to_storm_with_axi_tier(self):
        """Test: add fissure to storm fissures with axi tier."""
        self.data['is_storm'] = True
        self.data['tier'] = data.TIERS[3]
        fissure = Fissure(**self.data)

        self.assertEqual(len(self.storage._storm_fissures['axi']), 0)

        self.storage.add(fissure)

        self.assertEqual(len(self.storage._storm_fissures['axi']), 1)

    def test_add_to_hard_with_lith_tier(self):
        """Test: add fissure to hard fissures with lith tier."""
        self.data['is_hard'] = True
        fissure = Fissure(**self.data)

        self.assertEqual(len(self.storage._hard_fissures['lith']), 0)

        self.storage.add(fissure)

        self.assertEqual(len(self.storage._hard_fissures['lith']), 1)

    def test_add_to_hard_with_meso_tier(self):
        """Test: add fissure to hard fissures with meso tier."""
        self.data['is_hard'] = True
        self.data['tier'] = data.TIERS[1]
        fissure = Fissure(**self.data)

        self.assertEqual(len(self.storage._hard_fissures['meso']), 0)

        self.storage.add(fissure)

        self.assertEqual(len(self.storage._hard_fissures['meso']), 1)

    def test_add_to_hard_with_neo_tier(self):
        """Test: add fissure to hard fissures with neo tier."""
        self.data['is_hard'] = True
        self.data['tier'] = data.TIERS[2]
        fissure = Fissure(**self.data)

        self.assertEqual(len(self.storage._hard_fissures['neo']), 0)

        self.storage.add(fissure)

        self.assertEqual(len(self.storage._hard_fissures['neo']), 1)

    def test_add_to_hard_with_axi_tier(self):
        """Test: add fissure to hard fissures with axi tier."""
        self.data['is_hard'] = True
        self.data['tier'] = data.TIERS[3]
        fissure = Fissure(**self.data)

        self.assertEqual(len(self.storage._hard_fissures['axi']), 0)

        self.storage.add(fissure)

        self.assertEqual(len(self.storage._hard_fissures['axi']), 1)

    def test_add_to_kuva(self):
        """Test: add fissure to simple fissures with lith tier."""
        self.data['tier'] = data.TIERS[4]
        self.data['location'] = data.LOCATIONS[-8]
        fissure = Fissure(**self.data)

        self.assertEqual(len(self.storage._kuva_fissures), 0)

        self.storage.add(fissure)

        self.assertEqual(len(self.storage._kuva_fissures), 1)

    def test_get_all_fissure_list(self):
        """Test: get_all_fissure_list returns list of all fissures."""
        self.fill_storage()

        list_ = self.storage.get_all_fissure_list()

        self.assertIsInstance(list_, list)
        self.assertEqual(len(list_), 13)

    def test_get_all_ids(self):
        """Test: get_all_ids returns set of all fissure ids."""
        self.fill_storage()

        list_ = self.storage.get_all_ids()

        self.assertIsInstance(list_, list)
        self.assertEqual(len(list_), 13)

    def test_delete_fissure(self):
        """Test: delete_fissure."""
        fissure = Fissure(**self.data)
        self.storage.add(fissure)

        self.assertEqual(len(self.storage.get_all_fissure_list()), 1)

        self.storage.delete_fissure(fissure)

        self.assertEqual(len(self.storage.get_all_fissure_list()), 0)

    def test_get_fissures_returns_correct_values(self):
        """Test: get_fissures returns list of fissures by type."""
        self.fill_storage()

        for type in ('simple', 'storm', 'hard'):
            fissures = self.storage.get_fissures(type)
            self.assertIsInstance(fissures, dict)
            self.assertEqual(len(fissures), 4)
            for tier in ('lith', 'meso', 'neo', 'axi'):
                self.assertEqual(len(fissures[tier]), 1)

        self.assertIsInstance(self.storage.get_fissures('kuva'), list)
        self.assertEqual(len(self.storage.get_fissures('kuva')), 1)

    def test_get_fissures_get_raise_error(self):
        self.assertRaisesRegex(NameError, r'Type can be only simple, storm, hard or kuva.', self.storage.get_fissures,
                               None)


if __name__ == '__main__':
    unittest.main()
