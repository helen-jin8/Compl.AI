import { createBrowserRouter, Navigate } from 'react-router'
import LandingScreen from './screens/LandingScreen'
import FormScreen from './screens/FormScreen'
import QuestionsScreen from './screens/QuestionsScreen'
import GeneratingScreen from './screens/GeneratingScreen'
import ReportLayout from './screens/report/ReportLayout'
import SummarySection from './screens/report/SummarySection'
import FollowUpSection from './screens/report/FollowUpSection'
import StandardsSection from './screens/report/StandardsSection'
import LabsSection from './screens/report/LabsSection'
import FeedbackSection from './screens/report/FeedbackSection'

export const router = createBrowserRouter([
  { path: '/', Component: LandingScreen },
  { path: '/start', Component: FormScreen },
  { path: '/questions', Component: QuestionsScreen },
  { path: '/generating', Component: GeneratingScreen },
  {
    path: '/report',
    Component: ReportLayout,
    children: [
      { index: true, element: <Navigate to="/report/summary" replace /> },
      { path: 'summary', Component: SummarySection },
      { path: 'followups', Component: FollowUpSection },
      { path: 'standards', Component: StandardsSection },
      { path: 'labs', Component: LabsSection },
      { path: 'feedback', Component: FeedbackSection },
    ],
  },
  { path: '*', element: <Navigate to="/" replace /> },
])
