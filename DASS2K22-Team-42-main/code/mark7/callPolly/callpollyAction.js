function(properties, context) {

	const s3c = require("@aws-sdk/client-s3");
	const pc = require("@aws-sdk/client-polly");
	
    
	const REGION = "ap-south-1";
	const text = properties.inp;
    
	function sleep(ms) {
		return new Promise(resolve => setTimeout(resolve, ms));
	}
    
	const config = {
		credentials			: {
			accessKeyId		: "AKIA4AC4F4NFAQ4WCIDP",
			secretAccessKey	: "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"
		},
		region				: REGION
	}

	const s3Client = new s3c.S3Client( config );
	const pollyClient = new pc.PollyClient( config );
    
    const input1 = {
		OutputFormat		: "mp3",
		OutputS3BucketName	: "merrativetts",
		Text				: text,
		VoiceId				: "Aditi"
	}

	let data = context.async(async callback => {
		try{
			let data = await pollyClient.send( new pc.StartSpeechSynthesisTaskCommand(input1) );
			callback(null, data);
		}
		catch(err){
			callback(err);
		}
	});
	var KEY = "" + data.SynthesisTask.TaskId + ".mp3";
    const URL = "https://merrativetts.s3.ap-south-1.amazonaws.com/"+KEY;


	const params = {
		Bucket: "merrativetts",
		Key: KEY
	};
	const aclReq = {
		Bucket: "merrativetts",
		Key: KEY,
		ACL: "public-read"
	};

	context.async(async callback => {
		try{
			let existance = await s3c.waitUntilObjectExists( {client: s3Client, maxWaitTime: 60, maxDelay: 1, minDelay: 1}, params );
			callback(null, existance);
		}
		catch(err){
			callback(err);
		}
	});

	let madePublic = context.async(async callback => {
		try{
			let madePublic = await s3Client.send( new s3c.PutObjectAclCommand( aclReq ) );
			callback(null, madePublic);
		}
		catch(err){
			callback(err);
		}
	});
    
    return { url: URL, isvalid: true };
}
