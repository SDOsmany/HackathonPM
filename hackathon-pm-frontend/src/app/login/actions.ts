'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

import { createClient } from '@utils/supabase/server'
import { getUserFriendlyErrorMessage } from '@utils/errorHandling/authErrorMessages';

export async function login(formData: FormData) {
  const supabase = await createClient()

  // type-casting here for convenience
  // in practice, you should validate your inputs
  const data = {
    email: formData.get('email') as string,
    password: formData.get('password') as string,
  }

  const { error } = await supabase.auth.signInWithPassword(data)

  if (error) {
    const userFriendlyMessage = getUserFriendlyErrorMessage(error.message);
    redirect(`/login?error=${encodeURIComponent(userFriendlyMessage)}`);
  }

  revalidatePath('/', 'layout')
  redirect('/')
}

export async function signup(formData: FormData) {
  const supabase = await createClient()

  // type-casting here for convenience
  // in practice, you should validate your inputs
  const data = {
    email: formData.get('email') as string,
    password: formData.get('password') as string,
  }

  const { error } = await supabase.auth.signUp(data)

  if (error) {
    const userFriendlyMessage = getUserFriendlyErrorMessage(error.message);
    redirect(`/login?error=${encodeURIComponent(userFriendlyMessage)}`);
  }

  revalidatePath('/', 'layout')
  redirect('/')
}