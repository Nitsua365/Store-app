

export default function redisHashToJSON(hashList, hashFieldName) {
    hashList = hashList.filter(item => typeof item !== 'number')

    // get the ASIN's
    let filter = hashList.filter(m => (!Array.isArray(m)))
            
    // get the arrays of data and squash them into a list of JSON objects
    let arrays = hashList.filter(m => Array.isArray(m)).map(obj => {
        const keys = obj.filter((obj, filIdx) => (filIdx % 2 == 0) )
        const values = obj.filter((obj, valIdx) => (valIdx % 2 == 1 || !obj))

        let zipped = {}
        keys.forEach((key, idx) => zipped[key] = values[idx])

        return zipped;
    })
    
    // zip the hash and the data together
    return filter.map((obj, idx) => ({ [hashFieldName]: obj.substring(obj.indexOf(':') + 1), ...arrays[idx] }))
}