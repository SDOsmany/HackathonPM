/*
Gemini explanation of this class:
Okay, let's break down the Supabase middleware code you provided. You're right, this is the standard and recommended way to handle authentication sessions with Supabase in the Next.js App Router.
It might seem a little simple at first glance (return await updateSession(request)), but the power is hidden inside that updateSession function from @utils/supabase/middleware.
Here's what's happening and why it works for route protection:
1. The Role of middleware.ts in Next.js App Router:

The middleware.ts file (located at the root of your project, next to app, pages, etc.) is a special file that Next.js recognizes.
The function you export default from this file runs for every incoming request to your application (filtered by the config.matcher).
It allows you to intercept requests before they reach your page.tsx files or route.ts API handlers.
You can then perform logic like checking authentication, redirecting users, modifying request/response headers, etc.
2. The Supabase updateSession Helper Function:

The code import { updateSession } from '@/utils/supabase/middleware' tells you that Supabase provides a utility function specifically designed for use in Next.js middleware. You would typically have this updateSession function defined in a file like utils/supabase/middleware.ts.
What updateSession(request) typically does:

It internally creates a Supabase client instance that is configured to read the session cookie from the incoming request.
It reads the user's session information from the cookie set by Supabase after a successful login.
Crucially for session management: It might check if the session needs refreshing (e.g., if it's about to expire) and potentially update the session cookie. This helps maintain a smooth logged-in experience.
For route protection (your goal): Inside this updateSession function, it will also check if a session exists. If the request is for a protected route and no session is found, this function is designed to return a NextResponse.redirect() to your configured login page.
If a session is found, or if the request is for a public path (like /login), it returns NextResponse.next(), allowing the request to proceed to the intended page or API route.
It also handles making the authenticated Supabase client available later in the request lifecycle (e.g., in Server Components or Server Actions) so you can easily fetch user data or interact with Supabase services as the logged-in user.


In simple terms, the updateSession function is doing the heavy lifting of:

Reading the user's authentication state from the cookie.
Managing the session lifecycle (refreshing if needed).
Performing the necessary redirects if an unauthenticated user tries to access a protected resource.
Making the authenticated user information available for subsequent server-side code.
3. The export const config = { matcher: [...] }:

This configures which paths the middleware function should run on.
The regular expression /((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*) is designed to be very broad, matching almost all paths, but explicitly excluding common paths for static assets (like JavaScript, CSS, images, fonts) and Next.js internal files (_next/*).
This is an optimization so your middleware doesn't run unnecessarily for files that don't need authentication checks.
How this Achieves Route Protection:

A user requests a page, e.g., /dashboard.
The middleware.ts file runs because /dashboard matches the config.matcher.
The updateSession(request) function is called.
Inside updateSession, it checks for a Supabase session cookie.
If there's no valid session, updateSession generates and returns a NextResponse.redirect('/login').
The main middleware function receives this redirect response and returns it.
Next.js sees the redirect response and instructs the user's browser to navigate to /login. The user never reaches the /dashboard page.
If there is a valid session, updateSession returns NextResponse.next().
The main middleware function receives NextResponse.next() and returns it.
Next.js allows the request to proceed, and the /dashboard/page.tsx component is rendered.
*/

import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function updateSession(request: NextRequest) {
  let supabaseResponse = NextResponse.next({
    request,
  })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) => request.cookies.set(name, value))
          supabaseResponse = NextResponse.next({
            request,
          })
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          )
        },
      },
    }
  )

  // Do not run code between createServerClient and
  // supabase.auth.getUser(). A simple mistake could make it very hard to debug
  // issues with users being randomly logged out.

  // IMPORTANT: DO NOT REMOVE auth.getUser()

  const {
    data: { user },
  } = await supabase.auth.getUser()

  if (
    !user &&
    !request.nextUrl.pathname.startsWith('/login') &&
    !request.nextUrl.pathname.startsWith('/auth')
  ) {
    // no user, potentially respond by redirecting the user to the login page
    const url = request.nextUrl.clone()
    url.pathname = '/login'
    return NextResponse.redirect(url)
  }

  // IMPORTANT: You *must* return the supabaseResponse object as it is.
  // If you're creating a new response object with NextResponse.next() make sure to:
  // 1. Pass the request in it, like so:
  //    const myNewResponse = NextResponse.next({ request })
  // 2. Copy over the cookies, like so:
  //    myNewResponse.cookies.setAll(supabaseResponse.cookies.getAll())
  // 3. Change the myNewResponse object to fit your needs, but avoid changing
  //    the cookies!
  // 4. Finally:
  //    return myNewResponse
  // If this is not done, you may be causing the browser and server to go out
  // of sync and terminate the user's session prematurely!

  return supabaseResponse
}