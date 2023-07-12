let login = document.querySelector('.login_js'),
    register = document.querySelector('.register_js'),
    loginWindow = document.querySelector('.login'),
    registerWindow = document.querySelector('.registration'),
    input = document.querySelectorAll('input'),
    error = document.querySelectorAll('.error')

if (error) {
    input.forEach(input => {
        input.addEventListener('input', () => {
            error.forEach(error => {
                error.innerHTML = ''
            })
        })
    })
}

if (register) {
    register.addEventListener('click', () => {
        registerWindow.style.display = 'flex'
        loginWindow.style.display = 'none'
    })

    login.addEventListener('click', () => {
        loginWindow.style.display = 'flex'
        registerWindow.style.display = 'none'
    })
}

let nextUser = document.querySelector('.next_user'),
    prevUser = document.querySelector('.prev_user'),
    userNumber = document.querySelectorAll('.index_user'),
    left = 0, withCalc = 0

if (userNumber && nextUser) {
    withCalc = (userNumber.length - 8) * -80

    if (userNumber.length > 8) {
        nextUser.style.display = 'flex'
    }

    nextUser.addEventListener('click', () => {
        prevUser.style.display = 'flex'
        left -= 80
        userNumber.forEach(userNumber => {
            userNumber.style.left = `${left}px`
        })
        if (left === withCalc) {
            nextUser.style.display = 'none'
        }
    })
    prevUser.addEventListener('click', () => {
        nextUser.style.display = 'flex'
        left += 80
        userNumber.forEach(userNumber => {
            userNumber.style.left = `${left}px`
        })
        if (left === 0) {
            prevUser.style.display = 'none'
        }
    })
}

let video = document.querySelectorAll('video'),
    playVideo = document.querySelectorAll('.video_play')

if (playVideo) {
    playVideo.forEach((play, index) => {
        play.addEventListener('click', () => {
            video.forEach(vd => {
                vd.pause()
            })
            playVideo.forEach(play => {
                play.style.opacity = '1'
                play.style.zIndex = '2'
            })
            video[index].play()
            play.style.opacity = '0'
            play.style.zIndex = '-1'
        })
    })
    video.forEach((vd, index) => {
        vd.addEventListener('click', () => {
            vd.pause()
            playVideo[index].style.opacity = '1'
            playVideo[index].style.zIndex = '2'
        })
        vd.addEventListener('ended', () => {
            playVideo[index].style.opacity = '1'
            playVideo[index].style.zIndex = '2'
        })
    })
}

let heart = document.querySelectorAll('.heart'),
    postId = document.querySelectorAll('.none_post_id')

if (heart) {
    heart.forEach((heart, index) => {
        if (heart.innerHTML.search('i') === -1) {
            heart.innerHTML = `<a href="/add_like/${postId[index].innerHTML}" >
                                    <i class="fa-regular fa-heart" style="font-size: 24px"></i>
                                </a>`
        }

        heart.addEventListener('click', () => {
            if (heart.innerHTML === '<i class="fa-regular fa-heart"></i>') {
                heart.innerHTML = '<i class="fa-solid fa-heart" style="color: red"></i>'
            } else if (heart.innerHTML === '<i class="fa-solid fa-heart" style="color: red"></i>') {
                heart.innerHTML = '<i class="fa-regular fa-heart"></i>'
            }
        })
    })
}

let commentInput = document.querySelectorAll('.add_commentary input'),
    commentBtn = document.querySelectorAll('.add_commentary button')

commentInput.forEach((input, index) => {
    input.addEventListener('input', () => {
        if (input.value === '') {
            commentBtn[index].style.display = 'none'

        } else {
            commentBtn[index].style.display = 'block'
        }
    })
})

let editImg = document.querySelector('.edit_img_btn'),
    editImgWindow = document.querySelector('.edit_img'),
    exitImg = document.querySelector('.exit_img')

if (editImg) {
    editImg.addEventListener('click', () => {
        editImgWindow.style.display = ' flex'
    })
    exitImg.addEventListener('click', () => {
        editImgWindow.style.display = 'none'
    })
}

let allRecUser = document.querySelectorAll('.recommendation_box'),
    allRecUserBtn = document.querySelector('.all_user_index')

if (allRecUserBtn) {
    if (allRecUser.length < 7) {
        allRecUserBtn.style.display = 'none'
    }
    allRecUser.forEach((user, index) => {
        if (index >= 5) {
            user.style.display = 'none'
        } else {
            user.style.display = 'flex'
        }
    })
    allRecUserBtn.addEventListener('click', () => {
        allRecUser.forEach(user => {
            user.style.display = 'flex'
        })
        allRecUserBtn.style.display = 'none'
    })

}

let addPost = document.querySelector('.add_post_section'),
    addPostXmark = document.querySelector('.add_post_section .fa-xmark'),
    creatPost = document.querySelector('.creat_post')

if (addPost) {
    creatPost.addEventListener('click', () => {
        addPost.style.display = 'flex'
    })
    addPostXmark.addEventListener('click', () => {
        addPost.style.display = 'none'
    })
}

let postBio = document.querySelectorAll('.post_bio_js'),
    btnBio = document.querySelectorAll('.all_commentary')

if (postBio) {
    postBio.forEach((post, index) => {
        if (post.innerHTML.length < 209) {
            btnBio[index].style.display = 'none'
        }
    })
    btnBio.forEach((btn, index) => {
        btn.addEventListener('click', () => {
            postBio[index].style.height = 'auto'
            postBio[index].style.overflow = 'inherit'
            btn.style.display = 'none'
        })
    })
}

let aboutReels = document.querySelectorAll('.about_reels')

if (aboutReels) {
    aboutReels.forEach(bio => {
        let info = bio.innerHTML
        console.log(info.length)
        if (info.length > 400) {
            bio.innerHTML = info.slice(400) + '...'
        }
    })
}

let storyName = document.querySelectorAll('.index_user p')

if (storyName) {
    storyName.forEach(p => {
        if (p.innerHTML.length > 11) {
            p.innerHTML = p.innerHTML.slice(0, 9) + '..'
        }
    })
}

let followWindow = document.querySelector('.follow_or_follower_modal_window'),
    followBox = document.querySelectorAll('.user_follow_window'),
    followWindowBtn = document.querySelectorAll('.follow_window'),
    followWindowXmark = document.querySelectorAll('.window_row i')

if (followWindow) {
    followWindowBtn.forEach((btn, index) => {
        btn.addEventListener('click', () => {
            followWindow.style.display = 'flex'
            followBox[index].style.display = 'flex'
        })
    })
    followWindowXmark.forEach(xmark => {
        xmark.addEventListener('click', () => {
            followWindow.style.display = 'none'
            followBox.forEach(box => {
                box.style.display = 'none'
            })
        })
    })
}

let userActive = document.querySelectorAll('.pun_info_name'),
    userActiveWindow = document.querySelectorAll('.publication_video')

if (userActive) {
    userActive.forEach((btn, index) => {
        btn.addEventListener('click', () => {
            userActive.forEach(btn => {
                btn.classList.remove('border_active')
            })
            btn.classList.add('border_active')
            userActiveWindow.forEach(window => {
                window.style.display =' none'
            })
            userActiveWindow[index].style.display = 'flex'
        })
    })
}

