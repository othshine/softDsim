export function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

export const role = {
    ADMIN: "admin",
    STAFF: "staff",
    CREATOR: "creator",
    STUDENT: "student"
}