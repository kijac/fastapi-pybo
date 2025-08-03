import { writable } from 'svelte/store'

const persist_storage = (key, initValue) => {
    let storedValue = initValue
    
    // 브라우저 환경에서만 localStorage 사용
    if (typeof window !== 'undefined' && window.localStorage) {
        const storedValueStr = localStorage.getItem(key)
        if (storedValueStr != null) {
            try {
                storedValue = JSON.parse(storedValueStr)
            } catch (e) {
                storedValue = initValue
            }
        }
    }
    
    const store = writable(storedValue)
    
    // 브라우저 환경에서만 localStorage에 저장
    if (typeof window !== 'undefined' && window.localStorage) {
        store.subscribe((val) => {
            localStorage.setItem(key, JSON.stringify(val))
        })
    }
    
    return store
}

export const page = persist_storage("page", 0)
export const keyword = persist_storage("keyword", "")
export const access_token = persist_storage("access_token", "")
export const username = persist_storage("username", "")
export const is_login = persist_storage("is_login", false)