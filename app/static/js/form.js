async function getName() {
    const res = await fetch('/name')
    return res.text();
}

async function setName(name) {
    const res = await fetch('/name', {
        method: 'POST',
        body: JSON.stringify({ name }),
        headers: { 'Content-Type': 'application/json' }
    })
    return res.text();
}

Vue.createApp({
    data() {
        return { name : '' }
    },
    async mounted() {
        this.name = await getName();
    },
    methods: {
        async onEditNameSubmit(event) {
            this.name = await setName(this.name);
        }
    }
}).mount('#edit-name-form');
