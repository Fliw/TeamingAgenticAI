'use client'

import Link from 'next/link'
import { motion, Variants } from 'framer-motion'
import Icon from '@/components/ui/icon'
import { IconType } from '@/components/ui/icon/types'
import React, { useState } from 'react'
import { useQueryState } from 'nuqs'
import useAIChatStreamHandler from '@/hooks/useAIStreamHandler'
import { useStore } from '@/store'

const EXTERNAL_LINKS = {
  documentation: 'https://agno.link/agent-ui',
  agenOS: 'https://os.agno.com',
  agno: 'https://agno.com'
}

const TECH_ICONS = [
  {
    type: 'nextjs' as IconType,
    position: 'left-0',
    link: 'https://nextjs.org',
    name: 'Next.js',
    zIndex: 10
  },
  {
    type: 'shadcn' as IconType,
    position: 'left-[15px]',
    link: 'https://ui.shadcn.com',
    name: 'shadcn/ui',
    zIndex: 20
  },
  {
    type: 'tailwind' as IconType,
    position: 'left-[30px]',
    link: 'https://tailwindcss.com',
    name: 'Tailwind CSS',
    zIndex: 30
  }
]

interface ActionButtonProps {
  href: string
  variant?: 'primary'
  text: string
}

const ActionButton = ({ href, variant, text }: ActionButtonProps) => {
  const baseStyles =
    'px-4 py-2 text-sm transition-colors font-dmmono tracking-tight'
  const variantStyles = {
    primary: 'border border-border hover:bg-neutral-800 rounded-xl'
  }

  return (
    <Link
      href={href}
      target="_blank"
      className={`${baseStyles} ${variant ? variantStyles[variant] : ''}`}
    >
      {text}
    </Link>
  )
}

// Mapping pertanyaan berdasarkan nama team/agent
const QUESTION_MAP: Record<string, string[]> = {
  miko: [
    'Kamu punya member apa aja?',
    'Kemampuan membermu apa aja?',
    'Siapa yang bisa bantu urusan akademik?',
    'Siapa yang handle masalah keuangan?',
    'Apa aja yang bisa kamu bantu?',
    'Jelasin tentang team kamu dong'
  ],
  dakdak: [
    'Cara cek KRS gimana?',
    'Info tentang jadwal kuliah',
    'Info tentang sistem nilai akademik',
    'Bantu urusan administrasi akademik dong',
    'Cara daftar mata kuliah gimana?',
    'Info tentang administrasi akademik'
  ],
  kiko: [
    'Info tentang biaya kuliah',
    'Cara bayar uang kuliah gimana?',
    'Ada beasiswa yang bisa didaftar?',
    'Bantu urusan keuangan dong',
    'Info tentang tagihan kuliah',
    'Info tentang pembayaran dan beasiswa'
  ],
  lumi: [
    'Bantu bikin skripsi dong',
    'Cari topik penelitian yang menarik',
    'Cari jurnal tentang topik ini',
    'Cara mulai penelitian gimana?',
    'Bantu review paper penelitian',
    'Info tentang riset dan skripsi'
  ],
  nobi: [
    'Apa itu KRS dan bagaimana cara mengisinya?',
    'Bagaimana sistem perkuliahan di AMIKOM?',
    'Apa saja dokumen yang perlu disiapkan untuk registrasi?',
    'Bagaimana cara mengakses sistem akademik online?',
    'Apa saja kegiatan orientasi mahasiswa baru?',
    'Bagaimana prosedur registrasi mahasiswa baru?',
    'Kapan jadwal registrasi mahasiswa baru?',
    'Apa saja fasilitas kampus yang tersedia?'
  ]
}

// Default questions untuk team/agent yang tidak ada di mapping
const DEFAULT_TEAM_QUESTIONS = [
  'Kamu punya member apa aja?',
  'Kemampuan membermu apa aja?',
  'Apa aja yang bisa kamu bantu?',
  'Jelasin tentang team kamu dong'
]

const DEFAULT_AGENT_QUESTIONS = [
  'Apa aja yang bisa kamu bantu?',
  'Kemampuanmu apa aja?',
  'Bantu tugas kuliah dong',
  'Help me dengan project ini'
]

const getExampleQuestions = (
  entityName: string | undefined,
  mode: 'agent' | 'team'
): string[] => {
  if (!entityName) {
    return mode === 'team' ? DEFAULT_TEAM_QUESTIONS : DEFAULT_AGENT_QUESTIONS
  }

  const normalizedName = entityName.toLowerCase().trim()
  
  // Cek exact match
  if (QUESTION_MAP[normalizedName]) {
    return QUESTION_MAP[normalizedName]
  }

  // Cek partial match (misal "miko-team" akan match dengan "miko")
  for (const [key, questions] of Object.entries(QUESTION_MAP)) {
    if (normalizedName.includes(key) || key.includes(normalizedName)) {
      return questions
    }
  }

  // Default berdasarkan mode
  return mode === 'team' ? DEFAULT_TEAM_QUESTIONS : DEFAULT_AGENT_QUESTIONS
}

const ChatBlankState = () => {
  const [hoveredIcon, setHoveredIcon] = useState<string | null>(null)
  const { handleStreamResponse } = useAIChatStreamHandler()
  const [agentId] = useQueryState('agent')
  const [teamId] = useQueryState('team')
  const { mode, teams, agents } = useStore()
  const isEnabled = !!(agentId || teamId)

  // Get current entity (team or agent)
  const currentEntity = teamId
    ? teams.find((t) => t.id === teamId)
    : agentId
      ? agents.find((a) => a.id === agentId)
      : null

  const entityName = currentEntity?.name
  const exampleQuestions = getExampleQuestions(entityName, mode)

  const handleQuestionClick = async (question: string) => {
    if (!isEnabled) return
    try {
      await handleStreamResponse(question)
    } catch (error) {
      console.error('Error sending question:', error)
    }
  }

  // Animation variants for the icon
  const iconVariants: Variants = {
    initial: { y: 0 },
    hover: {
      y: -8,
      transition: {
        type: 'spring',
        stiffness: 150,
        damping: 10,
        mass: 0.5
      }
    },
    exit: {
      y: 0,
      transition: {
        type: 'spring',
        stiffness: 200,
        damping: 15,
        mass: 0.6
      }
    }
  }

  // Animation variants for the tooltip
  const tooltipVariants: Variants = {
    hidden: {
      opacity: 0,
      transition: {
        duration: 0.15,
        ease: 'easeInOut'
      }
    },
    visible: {
      opacity: 1,
      transition: {
        duration: 0.15,
        ease: 'easeInOut'
      }
    }
  }

  return (
    <section
      className="flex flex-col items-center text-center font-geist"
      aria-label="Welcome message"
    >
      <div className="flex max-w-3xl flex-col gap-y-8">
        <motion.h1
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="text-3xl font-[600] tracking-tight"
        >
          <div className="flex flex-col items-center justify-center gap-y-2 font-medium">
            <span className="flex items-center font-[600]">
              Halo, Mahasiswa AMIKOM! 👋
            </span>
            <span className="flex items-center font-[600] text-xl">
              Selamat datang di MIKO - Asisten AI Anda
            </span>
          </div>
          <p className="mt-4 text-lg text-muted">
            Mulai percakapan dengan AI untuk mendapatkan bantuan dalam pembelajaran dan tugas kuliah Anda
          </p>
        </motion.h1>
        {isEnabled && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.7 }}
            className="flex w-full flex-col gap-3"
          >
            <p className="text-sm font-medium text-muted">
              Coba tanya ini:
            </p>
            <div className="flex flex-wrap justify-center gap-2">
              {exampleQuestions.map((question, index) => (
                <motion.button
                  key={index}
                  onClick={() => handleQuestionClick(question)}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="rounded-xl border border-primary/15 bg-accent px-4 py-2 text-xs font-medium text-primary transition-colors hover:bg-accent/80 hover:border-primary/30"
                >
                  {question}
                </motion.button>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </section>
  )
}

export default ChatBlankState
