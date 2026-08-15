import { RouterProvider } from 'react-router'
import { ReportProvider } from './store/ReportContext'
import { router } from './routes'

export default function App() {
  return (
    <ReportProvider>
      <RouterProvider router={router} />
    </ReportProvider>
  )
}
