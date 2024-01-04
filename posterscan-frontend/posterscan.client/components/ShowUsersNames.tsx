'use client'
import getUsers from '@/app/constants/users';
import { useState, useEffect } from 'react'

type User = {
  id: number
  name: string
}

export default function ShowUsersName() {
  const [users, setUsers] = useState([])

  useEffect(() => {
    async function fetchUsers() {
      const users = await getUsers()
      setUsers(users)
    }
    fetchUsers()
  }, [])

  return (
    <div class="bg-gray-100 p-4 rounded-lg">
      <h2 class="text-lg font-bold text-blue-600">USERS</h2>
      <ul class="list-disc list-inside bg-white p-4 rounded shadow">
        {users.map((user: User) => (
          <li key={user.id} class="text-gray-700 hover:text-gray-900">
            {user.name}
          </li>
        ))}
      </ul>
    </div>
  )
}
