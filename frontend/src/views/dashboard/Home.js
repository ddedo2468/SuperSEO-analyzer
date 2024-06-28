import React from 'react'
import { Link } from 'react-router-dom'
import {
  CButton,
  CCard,
  CCardFooter,
  CCol,
  CRow,
  CBreadcrumb,
  CBreadcrumbItem,
  CFooter,
  CCardBody,
  CCardHeader,
} from '@coreui/react'

import WidgetsDropdown from '../widgets/WidgetsDropdown'
import MainChart from './MainChart'
import { Helmet } from 'react-helmet'

const Home = () => {
  const cardData = [
    { title: 'Analyzer', endpoint: '/seo-form' },
    { title: 'Keywords extractor', endpoint: '/keywords-extractor' },
  ]

  return (
    <>
      <Helmet>
        <title>Home - SEO Analyzer</title>
      </Helmet>

      <div className="ag-format-container">
        <div className="ag-tools_box">
          <div className="ag-tools_item">
            <Link to="/seo-form" className="ag-tools-item_link">
              <div className="ag-tools-item_bg"></div>

              <div className="ag-tools-item_title">Seo Analyzer</div>

              <div className="ag-tools-item_status-box">
                Status:
                <span className="ag-tools-item_status">Available</span>
              </div>
            </Link>
          </div>

          <div className="ag-tools_item">
            <Link to="/history" className="ag-tools-item_link">
              <div className="ag-tools-item_bg"></div>

              <div className="ag-tools-item_title">Analyzer History</div>

              <div className="ag-tools-item_status-box">
                Status:
                <span className="ag-tools-item_status">Available</span>
              </div>
            </Link>
          </div>

          <div className="ag-tools_item">
            <Link to="/web-crawler" className="ag-tools-item_link">
              <div className="ag-tools-item_bg"></div>

              <div className="ag-tools-item_title">web Crawler</div>

              <div className="ag-tools-item_status-box">
                Status:
                <span className="ag-tools-item_status">Avilable</span>
              </div>
            </Link>
          </div>
        </div>
      </div>
    </>
  )
}

export default Home
