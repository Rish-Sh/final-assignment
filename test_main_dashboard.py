import unittest
import pandas as pd
from unittest.mock import MagicMock, patch, create_autospec
from matplotlib.figure import Figure
import tkinter
from main_dashboard import update_dashboard_canvas, get_city_pair_data, plot_passenger_trips_trend,\
    compare_two_city_pairs_passenger_trip_trends
from data_cleaning_formatting import load_and_clean_data

class TestUpdateDashboardCanvas(unittest.TestCase):
    @patch('main_dashboard.FigureCanvasTkAgg')  # Use the correct module name here
    def test_update_dashboard_canvas(self, mock_figure_canvas):
        # Create a mock figure
        mock_fig = MagicMock(spec=Figure)

        # Create a mock canvas with the 'children' attribute
        mock_canvas = create_autospec(tkinter.Canvas, instance=True)
        mock_canvas.children = []

        # Call the function
        update_dashboard_canvas(mock_fig, mock_canvas)

        # Check if the FigureCanvasTkAgg was instantiated and drawn
        mock_figure_canvas.assert_called_with(mock_fig, master=mock_canvas)
        mock_figure_canvas.return_value.draw.assert_called()
        mock_figure_canvas.return_value.get_tk_widget().pack.assert_called_with(side='top', fill='both', expand=1)


class TestGetCityPairData(unittest.TestCase):
    def setUp(self):
        # Assuming load_and_clean_data returns a cleaned DataFrame
        self.sample_data = load_and_clean_data('dom_city_pair.csv')

    def test_correct_data_retrieval(self):
        result = get_city_pair_data('Adelaide', 'Brisbane')
        self.assertFalse(result.empty)
        self.assertEqual(len(result), 475)  # Assuming there's 1 row for this city pair


class TestPlotPassengerTripsTrend(unittest.TestCase):
    @patch('main_dashboard.sg.popup')  # Mock the popup function
    def test_empty_data(self, mock_popup):
        empty_data = pd.DataFrame()  # Create an empty DataFrame
        mock_canvas = create_autospec(tkinter.Canvas, instance=True)

        # Call the function with empty data
        plot_passenger_trips_trend(empty_data, mock_canvas)

        # Assert that the popup was called
        mock_popup.assert_called_once_with("No data found for the city pair")

    @patch('main_dashboard.update_dashboard_canvas')
    def test_non_empty_data(self, mock_update_canvas):
        # Create a non-empty DataFrame as sample data
        sample_data = pd.DataFrame({
            'City1': ['Adelaide'],
            'City2': ['Brisbane'],
            'Date': [pd.Timestamp('2020-01-01')],
            'Passenger_Trips': [100]
        })
        mock_canvas = create_autospec(tkinter.Canvas, instance=True)

        # Call the function with sample data
        plot_passenger_trips_trend(sample_data, mock_canvas)

        # Assert that the update_dashboard_canvas function was called
        self.assertTrue(mock_update_canvas.called)


class TestCompareTwoCityPairsPassengerTripTrends(unittest.TestCase):
    @patch('main_dashboard.get_city_pair_data')
    @patch('main_dashboard.update_dashboard_canvas')
    def test_both_city_pairs_have_data(self, mock_update_canvas, mock_get_city_pair_data):
        # Mock data for two city pairs
        mock_city_pair_data1 = pd.DataFrame({'Date': [1, 2, 3], 'Passenger_Trips': [100, 200, 300]})
        mock_city_pair_data2 = pd.DataFrame({'Date': [1, 2, 3], 'Passenger_Trips': [150, 250, 350]})
        mock_get_city_pair_data.side_effect = [mock_city_pair_data1, mock_city_pair_data2]

        mock_canvas = create_autospec(tkinter.Canvas, instance=True)

        # Call the function
        compare_two_city_pairs_passenger_trip_trends('CityA - CityB', 'CityC - CityD', mock_canvas)

        # Verify that the update_dashboard_canvas function was called
        mock_update_canvas.assert_called_once()

    @patch('main_dashboard.get_city_pair_data')
    @patch('main_dashboard.update_dashboard_canvas')
    def test_one_city_pair_has_data(self, mock_update_canvas, mock_get_city_pair_data):
        # Mock data for one city pair and None for another
        mock_city_pair_data = pd.DataFrame({'Date': [1, 2, 3], 'Passenger_Trips': [100, 200, 300]})
        mock_get_city_pair_data.side_effect = [mock_city_pair_data, None]

        mock_canvas = create_autospec(tkinter.Canvas, instance=True)

        # Call the function
        compare_two_city_pairs_passenger_trip_trends('CityA - CityB', 'CityC - CityD', mock_canvas)

        # Verify that the update_dashboard_canvas function was called
        mock_update_canvas.assert_called_once()

    @patch('main_dashboard.get_city_pair_data')
    @patch('main_dashboard.update_dashboard_canvas')
    def test_neither_city_pair_has_data(self, mock_update_canvas, mock_get_city_pair_data):
        # Mock get_city_pair_data to return None for both city pairs
        mock_get_city_pair_data.side_effect = [None, None]

        mock_canvas = create_autospec(tkinter.Canvas, instance=True)

        # Call the function
        compare_two_city_pairs_passenger_trip_trends('CityA - CityB', 'CityC - CityD', mock_canvas)

        # Verify that the update_dashboard_canvas function was not called
        mock_update_canvas.assert_not_called()


if __name__ == '__main__':
    unittest.main()

