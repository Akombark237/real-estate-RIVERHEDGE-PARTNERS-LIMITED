import { useState, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthContext } from '../context/AuthContext'

const About = () => {
  const { user } = useContext(AuthContext)
  const navigate = useNavigate()
  const [activeValue, setActiveValue] = useState(null)

  const coreValues = [
    {
      id: 'integrity',
      title: 'Integrity',
      icon: '🛡️',
      color: 'from-blue-600 to-blue-700',
      description: 'Integrity is the cornerstone of our operations. We uphold honesty, fairness, and transparency in every transaction, ensuring that our clients and partners can always trust our word. We conduct our business with ethical clarity, keeping our promises and maintaining open communication throughout every project phase. At Riverhedge Partners Limited, integrity isn\'t negotiable — it\'s our identity. It ensures that our relationships are built on a foundation of respect and mutual confidence that stands the test of time.'
    },
    {
      id: 'affordability',
      title: 'Affordability',
      icon: '💰',
      color: 'from-green-600 to-green-700',
      description: 'We believe that owning a quality home should be within reach for middle-income families. Affordability, to us, means delivering premium value without excessive cost. Through strategic planning, efficient sourcing, and innovative design, we make homeownership attainable while maintaining the highest standards of quality and safety. By controlling expenses responsibly, we enable clients to enjoy modern, durable homes that suit their budgets and aspirations.'
    },
    {
      id: 'efficiency',
      title: 'Efficiency',
      icon: '⚡',
      color: 'from-yellow-600 to-yellow-700',
      description: 'Efficiency is at the heart of how we operate. We are committed to using time, resources, and finances wisely to achieve maximum results with minimal waste. Our processes are streamlined to eliminate unnecessary delays, ensuring smooth project execution and timely delivery. Importantly, Riverhedge Partners Limited maintains financial discipline — we honor the same budget agreed upon at the start of each project, keeping it consistent until the end. There are no hidden charges or surprise cost increases.'
    },
    {
      id: 'timely-delivery',
      title: 'Timely Delivery',
      icon: '⏰',
      color: 'from-purple-600 to-purple-700',
      description: 'We understand that time is valuable. That\'s why we make punctuality a core promise. Our commitment to timely delivery reflects respect for our clients and partners who trust us to meet agreed deadlines. With proactive planning, constant communication, and an efficient work ethic, we ensure every property is completed and delivered on schedule — without compromising quality. At Riverhedge, reliability and timeliness are inseparable from professionalism.'
    },
    {
      id: 'customer-commitment',
      title: 'Customer Commitment',
      icon: '🤝',
      color: 'from-red-600 to-red-700',
      description: 'Our clients are at the center of everything we do. We dedicate ourselves to understanding their goals, guiding them through every stage of the property journey, and ensuring their satisfaction long after project completion. From first consultation to key handover, our approach is driven by empathy, transparency, and trust. We don\'t just sell properties — we build lifelong relationships founded on service, integrity, and genuine care.'
    },
    {
      id: 'innovation',
      title: 'Innovation',
      icon: '💡',
      color: 'from-indigo-600 to-indigo-700',
      description: 'Innovation fuels our growth and keeps us ahead in a fast-changing real estate market. We continuously explore modern construction methods, digital solutions, and sustainable technologies that enhance the living experience of our clients. By embracing creativity and forward-thinking, Riverhedge Partners Limited delivers housing solutions that are not only functional and beautiful but also future-ready.'
    },
    {
      id: 'community',
      title: 'Community Building',
      icon: '🏘️',
      color: 'from-teal-600 to-teal-700',
      description: 'We go beyond constructing homes — we build environments where families can connect, grow, and thrive. Our developments are designed with community life in mind: shared spaces, safety, accessibility, and local engagement. We partner with residents and local authorities to support neighborhood development, creating sustainable, inclusive communities that stand as a testament to our vision of long-term impact.'
    },
    {
      id: 'excellence',
      title: 'Excellence',
      icon: '⭐',
      color: 'from-orange-600 to-orange-700',
      description: 'Excellence is more than a goal; it is a daily pursuit. We aim to exceed expectations in everything we do — from the smallest detail in design to the final handover of a completed project. Our teams are driven by discipline, pride, and professionalism, ensuring that every home we deliver reflects our commitment to quality, durability, and client satisfaction.'
    },
    {
      id: 'empathy',
      title: 'Empathy',
      icon: '❤️',
      color: 'from-pink-600 to-pink-700',
      description: 'We approach every client relationship with compassion and understanding. By listening deeply to their needs and aspirations, we tailor our services to offer homes that truly fit their lives. Empathy allows us to build trust, resolve challenges with care, and create experiences that make every client feel valued, respected, and supported throughout their journey with Riverhedge Partners Limited.'
    },
    {
      id: 'financial-literacy',
      title: 'Financial Literacy Empowerment',
      icon: '📚',
      color: 'from-cyan-600 to-cyan-700',
      description: 'We believe that homeownership and wealth creation go hand in hand with knowledge. That\'s why we are committed to educating our clients about property investment, mortgages, and financial management. Through transparent communication, workshops, and expert guidance, we empower families to make informed, confident decisions that lead to lasting financial growth.'
    },
    {
      id: 'environmental',
      title: 'Environmental Stewardship',
      icon: '🌱',
      color: 'from-lime-600 to-lime-700',
      description: 'Our responsibility extends beyond business to the planet we all share. We integrate environmentally friendly practices into our construction and operations — from selecting sustainable materials to designing energy-efficient homes. Riverhedge Partners Limited is dedicated to promoting green living, reducing waste, and contributing positively to environmental preservation. By doing so, we not only create better homes but also a healthier, more sustainable world for future generations.'
    }
  ]

  return (
    <div className="px-4 py-6 sm:px-0">
      {/* Admin Edit Button */}
      {user && user.is_staff && (
        <div className="mb-4 flex justify-end">
          <button
            onClick={() => navigate('/about/edit')}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-md flex items-center"
          >
            <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Edit About Page
          </button>
        </div>
      )}

      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 via-blue-700 to-blue-800 rounded-xl shadow-2xl p-12 mb-8 relative overflow-hidden">
        <div className="absolute top-0 right-0 opacity-10">
          <svg className="h-64 w-64" fill="currentColor" viewBox="0 0 24 24">
            <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
          </svg>
        </div>
        <div className="relative z-10 text-center">
          <h1 className="text-5xl font-bold text-white mb-4">About Riverhedge Partners Limited</h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto">
            A real estate and investment company based in Abuja, Nigeria, focused on providing affordable housing solutions, 
            property development, and real estate investment advisory.
          </p>
        </div>
      </div>

      {/* Vision & Mission */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {/* Vision Card */}
        <div className="bg-white shadow-xl rounded-2xl p-8 border-t-4 border-purple-600">
          <div className="flex items-center mb-4">
            <div className="bg-purple-100 rounded-full p-3 mr-4">
              <svg className="h-8 w-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
            </div>
            <h2 className="text-3xl font-bold text-gray-900">Our Vision</h2>
          </div>
          <p className="text-gray-700 text-lg leading-relaxed">
            To become the most trusted and preferred real estate partner for middle-income families, recognized for delivering 
            exceptional homes, fostering community growth, and contributing to the economic and social well-being of the regions we serve.
          </p>
        </div>

        {/* Mission Card */}
        <div className="bg-white shadow-xl rounded-2xl p-8 border-t-4 border-green-600">
          <div className="flex items-center mb-4">
            <div className="bg-green-100 rounded-full p-3 mr-4">
              <svg className="h-8 w-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <h2 className="text-3xl font-bold text-gray-900">Our Mission</h2>
          </div>
          <p className="text-gray-700 text-lg leading-relaxed">
            At Riverhedge Partners Limited, our mission is to make quality homeownership accessible and affordable for middle-income families. 
            We are dedicated to creating vibrant, sustainable communities by offering well-designed, value-driven homes that meet the needs of modern living.
          </p>
        </div>
      </div>

      {/* Core Values Section */}
      <div className="bg-white shadow-xl rounded-2xl p-8 mb-8">
        <div className="text-center mb-8">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Our Core Values</h2>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            At Riverhedge Partners Limited, our values define who we are and guide every action we take. 
            They reflect our unwavering dedication to ethical business, customer satisfaction, and sustainable growth.
          </p>
        </div>

        {/* Values Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {coreValues.map((value) => (
            <div
              key={value.id}
              onClick={() => setActiveValue(activeValue === value.id ? null : value.id)}
              className={`cursor-pointer transition-all duration-300 rounded-xl p-6 ${
                activeValue === value.id
                  ? 'bg-gradient-to-br ' + value.color + ' text-white shadow-2xl transform scale-105'
                  : 'bg-gray-50 hover:bg-gray-100 hover:shadow-lg'
              }`}
            >
              <div className="text-center">
                <div className="text-5xl mb-3">{value.icon}</div>
                <h3 className={`text-xl font-bold mb-3 ${activeValue === value.id ? 'text-white' : 'text-gray-900'}`}>
                  {value.title}
                </h3>
                {activeValue === value.id && (
                  <p className="text-sm leading-relaxed text-white">
                    {value.description}
                  </p>
                )}
                {activeValue !== value.id && (
                  <p className="text-sm text-gray-500">Click to learn more</p>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Company Overview */}
      <div className="bg-gradient-to-r from-gray-800 to-gray-900 rounded-2xl shadow-xl p-8 mb-8 text-white">
        <h2 className="text-3xl font-bold mb-6 text-center">Company Overview</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="bg-white bg-opacity-10 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
              <svg className="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">Location</h3>
            <p className="text-gray-300">Based in Abuja, Nigeria</p>
          </div>
          <div className="text-center">
            <div className="bg-white bg-opacity-10 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
              <svg className="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">Focus</h3>
            <p className="text-gray-300">Affordable Housing Solutions</p>
          </div>
          <div className="text-center">
            <div className="bg-white bg-opacity-10 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
              <svg className="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">Target</h3>
            <p className="text-gray-300">Middle-Income Families</p>
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl shadow-xl p-12 text-center text-white">
        <h2 className="text-4xl font-bold mb-4">Join Us in Building Dreams</h2>
        <p className="text-xl mb-8 max-w-2xl mx-auto">
          Experience the Riverhedge difference — where integrity meets innovation, and your dream home becomes reality.
        </p>
        <div className="flex justify-center space-x-4">
          <button className="px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors shadow-lg">
            Explore Properties
          </button>
          <button className="px-8 py-3 bg-transparent border-2 border-white text-white rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors">
            Contact Us
          </button>
        </div>
      </div>
    </div>
  )
}

export default About

