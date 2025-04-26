// GSAP Animations
document.addEventListener('DOMContentLoaded', () => {
    // Fade-in animations
    gsap.utils.toArray('.gsap-fade-in').forEach((element, i) => {
        gsap.from(element, {
            opacity: 0,
            y: 50,
            duration: 1,
            delay: element.dataset.delay || i * 0.2,
            scrollTrigger: {
                trigger: element,
                start: 'top 80%',
                toggleActions: 'play none none none'
            }
        });
    });

    // Parallax effect
    gsap.utils.toArray('.parallax-bg').forEach(section => {
        gsap.to(section, {
            backgroundPositionY: '50%',
            ease: 'none',
            scrollTrigger: {
                trigger: section,
                scrub: true
            }
        });
    });

    // Micro-interactions: Book card hover
    document.querySelectorAll('.book-card').forEach(card => {
        card.addEventListener('mouseenter', () => {
            gsap.to(card, { scale: 1.05, boxShadow: '0 10px 20px rgba(0,0,0,0.2)', duration: 0.3 });
        });
        card.addEventListener('mouseleave', () => {
            gsap.to(card, { scale: 1, boxShadow: '0 4px 6px rgba(0,0,0,0.1)', duration: 0.3 });
        });
    });

    // Micro-interaction: Button hover
    document.querySelectorAll('.rent-button').forEach(button => {
        button.addEventListener('mouseenter', () => {
            gsap.to(button, { scale: 1.1, duration: 0.2 });
        });
        button.addEventListener('mouseleave', () => {
            gsap.to(button, { scale: 1, duration: 0.2 });
        });
    });

    // Micro-interaction: Table row hover
    document.querySelectorAll('.table-row').forEach(row => {
        row.addEventListener('mouseenter', () => {
            gsap.to(row, { backgroundColor: '#f3f4f6', duration: 0.2 });
        });
        row.addEventListener('mouseleave', () => {
            gsap.to(row, { backgroundColor: 'transparent', duration: 0.2 });
        });
    });

    // Ripple effect for buttons
    document.querySelectorAll('.ripple-button').forEach(button => {
        button.addEventListener('click', (e) => {
            const ripple = document.createElement('span');
            ripple.classList.add('absolute', 'bg-white', 'opacity-50', 'rounded-full', 'transform', 'scale-0');
            const diameter = Math.max(button.clientWidth, button.clientHeight);
            ripple.style.width = ripple.style.height = `${diameter}px`;
            const rect = button.getBoundingClientRect();
            ripple.style.left = `${e.clientX - rect.left - diameter / 2}px`;
            ripple.style.top = `${e.clientY - rect.top - diameter / 2}px`;
            button.appendChild(ripple);
            gsap.to(ripple, { scale: 2, opacity: 0, duration: 0.6, onComplete: () => ripple.remove() });
        });
    });

    // Search form loading spinner
    const searchForm = document.getElementById('search-form');
    const searchButton = document.getElementById('search-button');
    if (searchForm && searchButton) {
        searchForm.addEventListener('submit', () => {
            searchButton.innerHTML = '<svg class="animate-spin h-5 w-5 inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8h8a8 8 0 01-8 8 8 8 0 01-8-8z"></path></svg>';
            searchButton.disabled = true;
        });
    }

    // Open chatbot link
    const openChatbot = document.getElementById('open-chatbot');
    if (openChatbot) {
        openChatbot.addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelector('.botui-container').style.display = 'block';
        });
    }
});

// Three.js 3D Model
const initThreeJS = () => {
    const canvas = document.getElementById('threejs-canvas');
    if (!canvas) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    canvas.appendChild(renderer.domElement);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(0, 1, 1);
    scene.add(directionalLight);

    const loader = new THREE.GLTFLoader();
    loader.load(
        'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/BrainStem/glTF/BrainStem.gltf', // Replaced with a book model
        (gltf) => {
            const model = gltf.scene;
            model.scale.set(5, 5, 5); // Adjusted scale for book model
            model.position.set(0, 0, 0); // Center the model
            scene.add(model);

            document.addEventListener('mousemove', (event) => {
                const mouseX = (event.clientX / window.innerWidth) * 2 - 1;
                gsap.to(model.rotation, { y: mouseX * Math.PI * 0.5, duration: 1 });
            });
        },
        undefined,
        (error) => console.error('Error loading GLTF model:', error)
    );

    camera.position.z = 10; // Adjusted for book model size

    const animate = () => {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    };
    animate();

    window.addEventListener('resize', () => {
        camera.aspect = canvas.clientWidth / canvas.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    });
};
initThreeJS();

// Particles.js
particlesJS('particles-js', {
    particles: {
        number: { value: 80, density: { enable: true, value_area: 800 } },
        color: { value: '#ffffff' },
        shape: { type: 'circle' },
        opacity: { value: 0.5, random: false },
        size: { value: 3, random: true },
        line_linked: { enable: true, distance: 150, color: '#ffffff', opacity: 0.4, width: 1 },
        move: { enable: true, speed: 6, direction: 'none', random: false, straight: false, out_mode: 'out', bounce: false }
    },
    interactivity: {
        detect_on: 'canvas',
        events: { onhover: { enable: true, mode: 'repulse' }, onclick: { enable: true, mode: 'push' }, resize: true },
        modes: { repulse: { distance: 100, duration: 0.4 }, push: { particles_nb: 4 } }
    },
    retina_detect: true
});

// Onboarding Tour
const tour = new Shepherd.Tour({
    defaultStepOptions: {
        cancelIcon: { enabled: true },
        classes: 'shadow-md bg-purple-dark',
        scrollTo: { behavior: 'smooth', block: 'center' }
    }
});

tour.addStep({
    id: 'welcome',
    text: 'Welcome to Book Rental System! Let’s take a quick tour.',
    buttons: [{ text: 'Next', action: tour.next }]
});

tour.addStep({
    id: 'search',
    text: 'Use the search bar to find books by title, author, or ISBN.',
    attachTo: { element: '#search-form', on: 'bottom' },
    buttons: [{ text: 'Next', action: tour.next }, { text: 'Skip', action: tour.complete }]
});

tour.addStep({
    id: 'categories',
    text: 'Explore books by category to discover new reads.',
    attachTo: { element: 'a[href="/categories/"]', on: 'bottom' },
    buttons: [{ text: 'Next', action: tour.next }, { text: 'Skip', action: tour.complete }]
});

tour.addStep({
    id: 'account',
    text: 'Manage your account and view achievements here.',
    attachTo: { element: 'a[href="/account/"]', on: 'bottom' },
    buttons: [{ text: 'Finish', action: tour.complete }]
});

// Start tour for new users (simulated with localStorage)
if (!localStorage.getItem('tourCompleted')) {
    tour.start();
    localStorage.setItem('tourCompleted', 'true');
}

// Chatbot
const initChatbot = () => {
    const botui = new BotUI('chatbot');
    botui.message.add({
        content: 'Hello! I’m your Book Rental Assistant. How can I help you today?'
    }).then(() => {
        botui.action.button({
            action: [
                { text: 'How to rent a book?', value: 'rent' },
                { text: 'Find a book', value: 'find' },
                { text: 'Contact support', value: 'support' },
                { text: 'Check my rentals', value: 'rentals' },
                { text: 'Explore categories', value: 'categories' }
            ]
        }).then(res => {
            if (res.value === 'rent') {
                botui.message.add({
                    content: 'To rent a book, log in, browse or search for a book, and click "Rent This Book" on its detail page.'
                });
            } else if (res.value === 'find') {
                botui.message.add({
                    content: 'Use the search bar or visit the Categories page to find books.'
                });
            } else if (res.value === 'support') {
                botui.message.add({
                    content: 'Visit our Contact page or email support@bookrental.com.'
                });
            } else if (res.value === 'rentals') {
                botui.message.add({
                    content: 'Check your rental history on the Rental History page.'
                });
            } else if (res.value === 'categories') {
                botui.message.add({
                    content: 'Browse books by category on the Categories page, accessible from the navbar.'
                });
            }
        });
    });
};
initChatbot();