# coding: utf-8
#
# Copyright 2015 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for recommendations_services."""

__author__ = 'Xinyu Wu'

from core.domain import recommendations_services
from core.domain import rights_manager
from core.domain import user_services
from core.platform import models
(recommendations_models, exp_models,) = models.Registry.import_models([
    models.NAMES.recommendations, models.NAMES.exploration])
from core.tests import test_utils
import feconf


class TopicSimilarityUnitTests(test_utils.GenericTestBase):
    """Tests of the recommendation services module."""

    TOPIC_SIMILARITIES_DEFAULT = (
"""Architecture,Art,Biology,Business,Chemistry,Computing,Economics,Education,Engineering,Environment,Geography,Government,Hobbies,Languages,Law,Life Skills,Mathematics,Medicine,Music,Philosophy,Physics,Programming,Psychology,Puzzles,Reading,Religion,Sport,Statistics,Welcome
1.0,0.9,0.2,0.4,0.1,0.2,0.3,0.3,0.6,0.6,0.4,0.2,0.5,0.5,0.5,0.3,0.5,0.3,0.3,0.5,0.4,0.1,0.6,0.1,0.1,0.1,0.1,0.1,0.3
0.9,1.0,0.1,0.6,0.1,0.1,0.6,0.6,0.2,0.3,0.3,0.2,0.5,0.7,0.6,0.2,0.3,0.2,0.9,0.7,0.3,0.1,0.6,0.1,0.1,0.1,0.1,0.1,0.3
0.2,0.1,1.0,0.2,0.8,0.3,0.2,0.3,0.3,0.7,0.4,0.2,0.2,0.1,0.1,0.9,0.4,0.8,0.1,0.1,0.4,0.1,0.6,0.1,0.1,0.1,0.1,0.6,0.3
0.4,0.6,0.2,1.0,0.1,0.5,0.9,0.6,0.4,0.6,0.2,0.7,0.2,0.5,0.7,0.1,0.3,0.1,0.1,0.6,0.1,0.2,0.3,0.1,0.1,0.1,0.1,0.5,0.3
0.1,0.1,0.8,0.1,1.0,0.2,0.2,0.3,0.2,0.6,0.6,0.1,0.2,0.2,0.2,0.7,0.3,0.7,0.1,0.1,0.2,0.1,0.3,0.1,0.1,0.1,0.1,0.3,0.3
0.2,0.1,0.3,0.5,0.2,1.0,0.6,0.3,0.6,0.1,0.1,0.1,0.2,0.2,0.1,0.3,0.9,0.2,0.2,0.3,0.4,0.95,0.3,0.5,0.1,0.1,0.1,0.6,0.3
0.3,0.6,0.2,0.9,0.2,0.6,1.0,0.3,0.3,0.5,0.4,0.7,0.2,0.4,0.8,0.2,0.6,0.2,0.1,0.3,0.1,0.3,0.6,0.3,0.2,0.1,0.1,0.7,0.3
0.3,0.6,0.3,0.6,0.3,0.3,0.3,1.0,0.3,0.5,0.3,0.5,0.2,0.2,0.6,0.1,0.2,0.1,0.1,0.5,0.1,0.1,0.6,0.1,0.3,0.2,0.2,0.2,0.3
0.6,0.2,0.3,0.4,0.2,0.6,0.3,0.3,1.0,0.4,0.2,0.2,0.2,0.2,0.3,0.1,0.7,0.1,0.1,0.3,0.6,0.6,0.2,0.3,0.1,0.1,0.1,0.5,0.3
0.6,0.3,0.7,0.6,0.6,0.1,0.5,0.5,0.4,1.0,0.8,0.6,0.2,0.2,0.3,0.8,0.2,0.3,0.1,0.2,0.1,0.1,0.3,0.1,0.1,0.1,0.1,0.3,0.3
0.4,0.3,0.4,0.2,0.6,0.1,0.4,0.3,0.2,0.8,1.0,0.2,0.2,0.4,0.3,0.6,0.3,0.3,0.1,0.1,0.1,0.1,0.3,0.1,0.1,0.1,0.1,0.2,0.3
0.2,0.2,0.2,0.7,0.1,0.1,0.7,0.5,0.2,0.6,0.2,1.0,0.2,0.3,0.8,0.1,0.1,0.1,0.1,0.4,0.1,0.1,0.4,0.1,0.5,0.5,0.2,0.4,0.3
0.5,0.5,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,1.0,0.5,0.2,0.2,0.3,0.2,0.4,0.2,0.3,0.5,0.2,0.6,0.5,0.3,0.6,0.2,0.3
0.5,0.7,0.1,0.5,0.2,0.2,0.4,0.2,0.2,0.2,0.4,0.3,0.5,1.0,0.3,0.1,0.1,0.1,0.3,0.4,0.1,0.1,0.3,0.1,0.8,0.4,0.1,0.1,0.3
0.5,0.6,0.1,0.7,0.2,0.1,0.8,0.6,0.3,0.3,0.3,0.8,0.2,0.3,1.0,0.1,0.1,0.1,0.1,0.6,0.1,0.1,0.6,0.1,0.4,0.6,0.1,0.2,0.3
0.3,0.2,0.9,0.1,0.7,0.3,0.2,0.1,0.1,0.8,0.6,0.1,0.2,0.1,0.1,1.0,0.4,0.8,0.1,0.2,0.2,0.2,0.3,0.1,0.2,0.1,0.3,0.4,0.3
0.5,0.3,0.4,0.3,0.3,0.9,0.6,0.2,0.7,0.2,0.3,0.1,0.3,0.1,0.1,0.4,1.0,0.2,0.3,0.4,0.7,0.8,0.2,0.6,0.1,0.1,0.1,0.8,0.3
0.3,0.2,0.8,0.1,0.7,0.2,0.2,0.1,0.1,0.3,0.3,0.1,0.2,0.1,0.1,0.8,0.2,1.0,0.2,0.3,0.1,0.2,0.3,0.1,0.1,0.1,0.1,0.1,0.3
0.3,0.9,0.1,0.1,0.1,0.2,0.1,0.1,0.1,0.1,0.1,0.1,0.4,0.3,0.1,0.1,0.3,0.2,1.0,0.6,0.3,0.2,0.4,0.1,0.3,0.1,0.1,0.1,0.3
0.5,0.7,0.1,0.6,0.1,0.3,0.3,0.5,0.3,0.2,0.1,0.4,0.2,0.4,0.6,0.2,0.4,0.3,0.6,1.0,0.3,0.6,0.4,0.5,0.2,0.1,0.1,0.3,0.3
0.4,0.3,0.4,0.1,0.2,0.4,0.1,0.1,0.6,0.1,0.1,0.1,0.3,0.1,0.1,0.2,0.7,0.1,0.3,0.3,1.0,0.6,0.1,0.5,0.2,0.1,0.3,0.4,0.3
0.1,0.1,0.1,0.2,0.1,0.95,0.3,0.1,0.6,0.1,0.1,0.1,0.5,0.1,0.1,0.2,0.8,0.2,0.2,0.6,0.6,1.0,0.3,0.6,0.1,0.1,0.1,0.6,0.3
0.6,0.6,0.6,0.3,0.3,0.3,0.6,0.6,0.2,0.3,0.3,0.4,0.2,0.3,0.6,0.3,0.2,0.3,0.4,0.4,0.1,0.3,1.0,0.4,0.3,0.3,0.2,0.4,0.3
0.1,0.1,0.1,0.1,0.1,0.5,0.3,0.1,0.3,0.1,0.1,0.1,0.6,0.1,0.1,0.1,0.6,0.1,0.1,0.5,0.5,0.6,0.4,1.0,0.1,0.1,0.1,0.5,0.3
0.1,0.1,0.1,0.1,0.1,0.1,0.2,0.3,0.1,0.1,0.1,0.5,0.5,0.8,0.4,0.2,0.1,0.1,0.3,0.2,0.2,0.1,0.3,0.1,1.0,0.4,0.1,0.1,0.3
0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.2,0.1,0.1,0.1,0.5,0.3,0.4,0.6,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.3,0.1,0.4,1.0,0.2,0.1,0.3
0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.2,0.1,0.1,0.1,0.2,0.6,0.1,0.1,0.3,0.1,0.1,0.1,0.1,0.3,0.1,0.2,0.1,0.1,0.2,1.0,0.3,0.3
0.1,0.1,0.6,0.5,0.3,0.6,0.7,0.2,0.5,0.3,0.2,0.4,0.2,0.1,0.2,0.4,0.8,0.1,0.1,0.3,0.4,0.6,0.4,0.5,0.1,0.1,0.3,1.0,0.3
0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,1.0""")

    TOPIC_SIMILARITIES_UPDATED = (
"""Architecture,Art,Biology,Business,Chemistry,Computing,Economics,Education,Engineering,Environment,Geography,Government,Hobbies,Languages,Law,Life Skills,Mathematics,Medicine,Music,Philosophy,Physics,Programming,Psychology,Puzzles,Reading,Religion,Sport,Statistics,Welcome
1.0,0.9,0.2,0.4,0.1,0.2,0.3,0.3,0.6,0.6,0.4,0.2,0.5,0.5,0.5,0.3,0.5,0.3,0.3,0.5,0.4,0.1,0.6,0.1,0.1,0.1,0.1,0.1,0.3
0.9,1.0,0.2,0.6,0.1,0.1,0.6,0.6,0.2,0.3,0.3,0.2,0.5,0.7,0.6,0.2,0.3,0.2,0.9,0.7,0.3,0.1,0.6,0.1,0.1,0.1,0.1,0.1,0.3
0.2,0.2,1.0,0.2,0.8,0.3,0.2,0.3,0.3,0.7,0.4,0.2,0.2,0.1,0.1,0.9,0.4,0.8,0.1,0.1,0.4,0.1,0.6,0.1,0.1,0.1,0.1,0.6,0.3
0.4,0.6,0.2,1.0,0.1,0.5,0.9,0.6,0.4,0.6,0.2,0.7,0.2,0.5,0.7,0.1,0.3,0.1,0.1,0.6,0.1,0.2,0.3,0.1,0.1,0.1,0.1,0.5,0.3
0.1,0.1,0.8,0.1,1.0,0.2,0.2,0.3,0.2,0.6,0.6,0.1,0.2,0.2,0.2,0.7,0.3,0.7,0.1,0.1,0.2,0.1,0.3,0.1,0.1,0.1,0.1,0.3,0.3
0.2,0.1,0.3,0.5,0.2,1.0,0.6,0.3,0.6,0.1,0.1,0.1,0.2,0.2,0.1,0.3,0.9,0.2,0.2,0.3,0.4,0.95,0.3,0.5,0.1,0.1,0.1,0.6,0.3
0.3,0.6,0.2,0.9,0.2,0.6,1.0,0.3,0.3,0.5,0.4,0.7,0.2,0.4,0.8,0.2,0.6,0.2,0.1,0.3,0.1,0.3,0.6,0.3,0.2,0.1,0.1,0.7,0.3
0.3,0.6,0.3,0.6,0.3,0.3,0.3,1.0,0.3,0.5,0.3,0.5,0.2,0.2,0.6,0.1,0.2,0.1,0.1,0.5,0.1,0.1,0.6,0.1,0.3,0.2,0.2,0.2,0.3
0.6,0.2,0.3,0.4,0.2,0.6,0.3,0.3,1.0,0.4,0.2,0.2,0.2,0.2,0.3,0.1,0.7,0.1,0.1,0.3,0.6,0.6,0.2,0.3,0.1,0.1,0.1,0.5,0.3
0.6,0.3,0.7,0.6,0.6,0.1,0.5,0.5,0.4,1.0,0.8,0.6,0.2,0.2,0.3,0.8,0.2,0.3,0.1,0.2,0.1,0.1,0.3,0.1,0.1,0.1,0.1,0.3,0.3
0.4,0.3,0.4,0.2,0.6,0.1,0.4,0.3,0.2,0.8,1.0,0.2,0.2,0.4,0.3,0.6,0.3,0.3,0.1,0.1,0.1,0.1,0.3,0.1,0.1,0.1,0.1,0.2,0.3
0.2,0.2,0.2,0.7,0.1,0.1,0.7,0.5,0.2,0.6,0.2,1.0,0.2,0.3,0.8,0.1,0.1,0.1,0.1,0.4,0.1,0.1,0.4,0.1,0.5,0.5,0.2,0.4,0.3
0.5,0.5,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,1.0,0.5,0.2,0.2,0.3,0.2,0.4,0.2,0.3,0.5,0.2,0.6,0.5,0.3,0.6,0.2,0.3
0.5,0.7,0.1,0.5,0.2,0.2,0.4,0.2,0.2,0.2,0.4,0.3,0.5,1.0,0.3,0.1,0.1,0.1,0.3,0.4,0.1,0.1,0.3,0.1,0.8,0.4,0.1,0.1,0.3
0.5,0.6,0.1,0.7,0.2,0.1,0.8,0.6,0.3,0.3,0.3,0.8,0.2,0.3,1.0,0.1,0.1,0.1,0.1,0.6,0.1,0.1,0.6,0.1,0.4,0.6,0.1,0.2,0.3
0.3,0.2,0.9,0.1,0.7,0.3,0.2,0.1,0.1,0.8,0.6,0.1,0.2,0.1,0.1,1.0,0.4,0.8,0.1,0.2,0.2,0.2,0.3,0.1,0.2,0.1,0.3,0.4,0.3
0.5,0.3,0.4,0.3,0.3,0.9,0.6,0.2,0.7,0.2,0.3,0.1,0.3,0.1,0.1,0.4,1.0,0.2,0.3,0.4,0.7,0.8,0.2,0.6,0.1,0.1,0.1,0.8,0.3
0.3,0.2,0.8,0.1,0.7,0.2,0.2,0.1,0.1,0.3,0.3,0.1,0.2,0.1,0.1,0.8,0.2,1.0,0.2,0.3,0.1,0.2,0.3,0.1,0.1,0.1,0.1,0.1,0.3
0.3,0.9,0.1,0.1,0.1,0.2,0.1,0.1,0.1,0.1,0.1,0.1,0.4,0.3,0.1,0.1,0.3,0.2,1.0,0.6,0.3,0.2,0.4,0.1,0.3,0.1,0.1,0.1,0.3
0.5,0.7,0.1,0.6,0.1,0.3,0.3,0.5,0.3,0.2,0.1,0.4,0.2,0.4,0.6,0.2,0.4,0.3,0.6,1.0,0.3,0.6,0.4,0.5,0.2,0.1,0.1,0.3,0.3
0.4,0.3,0.4,0.1,0.2,0.4,0.1,0.1,0.6,0.1,0.1,0.1,0.3,0.1,0.1,0.2,0.7,0.1,0.3,0.3,1.0,0.6,0.1,0.5,0.2,0.1,0.3,0.4,0.3
0.1,0.1,0.1,0.2,0.1,0.95,0.3,0.1,0.6,0.1,0.1,0.1,0.5,0.1,0.1,0.2,0.8,0.2,0.2,0.6,0.6,1.0,0.3,0.6,0.1,0.1,0.1,0.6,0.3
0.6,0.6,0.6,0.3,0.3,0.3,0.6,0.6,0.2,0.3,0.3,0.4,0.2,0.3,0.6,0.3,0.2,0.3,0.4,0.4,0.1,0.3,1.0,0.4,0.3,0.3,0.2,0.4,0.3
0.1,0.1,0.1,0.1,0.1,0.5,0.3,0.1,0.3,0.1,0.1,0.1,0.6,0.1,0.1,0.1,0.6,0.1,0.1,0.5,0.5,0.6,0.4,1.0,0.1,0.1,0.1,0.5,0.3
0.1,0.1,0.1,0.1,0.1,0.1,0.2,0.3,0.1,0.1,0.1,0.5,0.5,0.8,0.4,0.2,0.1,0.1,0.3,0.2,0.2,0.1,0.3,0.1,1.0,0.4,0.1,0.1,0.3
0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.2,0.1,0.1,0.1,0.5,0.3,0.4,0.6,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.3,0.1,0.4,1.0,0.2,0.1,0.3
0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.2,0.1,0.1,0.1,0.2,0.6,0.1,0.1,0.3,0.1,0.1,0.1,0.1,0.3,0.1,0.2,0.1,0.1,0.2,1.0,0.3,0.3
0.1,0.1,0.6,0.5,0.3,0.6,0.7,0.2,0.5,0.3,0.2,0.4,0.2,0.1,0.2,0.4,0.8,0.1,0.1,0.3,0.4,0.6,0.4,0.5,0.1,0.1,0.3,1.0,0.3
0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,1.0""")

    def test_validate_default_similarities(self):
        recommendations_services._validate_topic_similarities(
            recommendations_services.DEFAULT_TOPIC_SIMILARITIES_STRING)

    def test_update_topic_similarities(self):
        recommendations_services.update_topic_similarities(
            'Art,Biology,Chemistry\n'
            '1.0,0.2,0.1\n'
            '0.2,1.0,0.8\n'
            '0.1,0.8,1.0')

        with self.assertRaisesRegexp(
                Exception, 'Length of topic similarities columns does not'
                           ' match topic list.'):
            recommendations_services.update_topic_similarities(
                'Art,Biology,Chemistry\n'
                '1.0,0.2,0.1\n'
                '0.2,1.0,0.8')

        with self.assertRaisesRegexp(
                Exception, 'Length of topic similarities rows does not match'
                           ' topic list.'):
            recommendations_services.update_topic_similarities(
                'Art,Biology,Chemistry\n'
                '1.0,0.2,0.1\n'
                '0.2,1.0\n'
                '0.1,0.8,1.0')

        with self.assertRaisesRegexp(
                ValueError, 'Expected similarity to be between 0.0 and 1.0,'
                            ' received 800'):
            recommendations_services.update_topic_similarities(
                'Art,Biology,Chemistry\n'
                '1.0,0.2,0.1\n'
                '0.2,1.0,800\n'
                '0.1,0.8,1.0')

        with self.assertRaisesRegexp(
                ValueError, 'Expected similarity to be a float, received'
                            ' string'):
            recommendations_services.update_topic_similarities(
                'Art,Biology,Chemistry\n'
                'string,0.2,0.1\n'
                '0.2,1.0,0.8\n'
                '0.1,0.8,1.0')

        with self.assertRaisesRegexp(
                Exception, 'Topic Fake Topic not in list of known topics.'):
            recommendations_services.update_topic_similarities(
                'Fake Topic,Biology,Chemistry\n'
                'string,0.2,0.1\n'
                '0.2,1.0,0.8\n'
                '0.1,0.8,1.0')

        with self.assertRaisesRegexp(
                Exception, 'Expected topic similarities to be symmetric.'):
            recommendations_services.update_topic_similarities(
                'Art,Biology,Chemistry\n'
                '1.0,0.2,0.1\n'
                '0.3,1.0,0.8\n'
                '0.8,0.1,1.0')

    def test_get_topic_similarity(self):
        self.assertEqual(recommendations_services.get_topic_similarity(
            'Art', 'Biology'), 0.1)
        self.assertEqual(recommendations_services.get_topic_similarity(
            'Art', 'Art'), feconf.SAME_TOPIC_SIMILARITY)
        self.assertEqual(recommendations_services.get_topic_similarity(
            'Topic 1', 'Topic 2'), feconf.DEFAULT_TOPIC_SIMILARITY)
        self.assertEqual(recommendations_services.get_topic_similarity(
            'Topic', 'Topic'), feconf.SAME_TOPIC_SIMILARITY)

        recommendations_services.update_topic_similarities(
            'Art,Biology,Chemistry\n'
            '1.0,0.2,0.1\n'
            '0.2,1.0,0.8\n'
            '0.1,0.8,1.0')
        self.assertEqual(recommendations_services.get_topic_similarity(
            'Art', 'Biology'), 0.2)

    def test_get_topic_similarities_as_csv(self):
        # The splitlines() is needed because a carriage return is added in
        # the returned string
        self.assertEqual(
            recommendations_services.get_topic_similarities_as_csv().splitlines(),
            self.TOPIC_SIMILARITIES_DEFAULT.splitlines())

        recommendations_services.update_topic_similarities(
            'Art,Biology,Chemistry\n'
            '1.0,0.2,0.1\n'
            '0.2,1.0,0.8\n'
            '0.1,0.8,1.0')
        self.assertEqual(
            recommendations_services.get_topic_similarities_as_csv().splitlines(),
            self.TOPIC_SIMILARITIES_UPDATED.splitlines())


class RecommendationsServicesUnitTests(test_utils.GenericTestBase):
    """Test recommendations services."""

    EXP_DATA = {
        'exp_id_1': {
            'category': 'Art',
        },
        'exp_id_2': {
            'category': 'Biology',
        },
        'exp_id_3': {
            'category': 'Chemistry',
        },
        'exp_id_4': {
            'category': 'Art',
        }
    }
    USER_DATA = {
        'alice': {
            'email': 'alice@example.com'
        },
        'bob': {
            'email': 'bob@example.com'
        },
        'charlie': {
            'email': 'charlie@example.com'
        },
    }

    def setUp(self):
        """Before each individual test, set up dummy explorations, users
        and admin."""
        super(RecommendationsServicesUnitTests, self).setUp()

        for name, user in self.USER_DATA.iteritems():
            user['id'] = self.get_user_id_from_email(
                user['email'])
            user_services.get_or_create_user(user['id'], user['email'])
            self.signup(user['email'], name)
            self.USER_DATA[name]['id'] = user['id']

        self.EXP_DATA['exp_id_1']['owner_id'] = self.USER_DATA['alice']['id']
        self.EXP_DATA['exp_id_2']['owner_id'] = self.USER_DATA['alice']['id']
        self.EXP_DATA['exp_id_3']['owner_id'] = self.USER_DATA['bob']['id']
        self.EXP_DATA['exp_id_4']['owner_id'] = self.USER_DATA['charlie']['id']

        for exp_id, exp in self.EXP_DATA.iteritems():
            self.save_new_valid_exploration(
                exp_id, exp['owner_id'], category=exp['category'])
            rights_manager.publish_exploration(exp['owner_id'], exp_id)

        self.ADMIN_ID = self.get_user_id_from_email(self.ADMIN_EMAIL)
        user_services.get_or_create_user(
            self.ADMIN_ID, self.ADMIN_EMAIL)
        self.signup(self.ADMIN_EMAIL, self.ADMIN_USERNAME)
        self.set_admins([self.ADMIN_EMAIL])


class ExplorationRecommendationsUnitTests(RecommendationsServicesUnitTests):
    """Test recommendations services relating to exploration comparison."""

    def test_get_item_similarity(self):
        with self.assertRaisesRegexp(
                Exception, 'Invalid reference_exp_id fake_exp_id'):
            recommendations_services.get_item_similarity(
                'fake_exp_id', 'fake_exp_id_2')

        self.assertEqual(recommendations_services.get_item_similarity(
            'exp_id_1', 'exp_id_2'), 4.5)
        self.assertEqual(recommendations_services.get_item_similarity(
            'exp_id_4', 'exp_id_4'), 9.0)

        rights_manager.publicize_exploration(self.ADMIN_ID, 'exp_id_4')
        self.assertEqual(recommendations_services.get_item_similarity(
            'exp_id_4', 'exp_id_4'), 10.0)

        rights_manager.unpublish_exploration(self.ADMIN_ID, 'exp_id_2')
        self.assertEqual(recommendations_services.get_item_similarity(
            'exp_id_1', 'exp_id_2'), 0.0)

    def test_get_and_set_exploration_recommendations(self):
        recommended_exp_ids = ['exp_id_2', 'exp_id_3']
        recommendations_services.set_recommendations(
            'exp_id_1', recommended_exp_ids)
        saved_recommendation_ids = (
            recommendations_services.get_exploration_recommendations(
                'exp_id_1'))
        self.assertEqual(recommended_exp_ids, saved_recommendation_ids)

        recommended_exp_ids = ['exp_id_3']
        recommendations_services.set_recommendations(
            'exp_id_1', recommended_exp_ids)
        saved_recommendation_ids = (
            recommendations_services.get_exploration_recommendations(
                'exp_id_1'))
        self.assertEqual(recommended_exp_ids, saved_recommendation_ids)
